# stdlib imports
import uuid
import random
import datetime

# django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils.timezone import utc
from django.core import urlresolvers

# local imports
from utils.hash import random_base36_string


class Lottery(models.Model):
    """Lottery model"""
    hash_key = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    registration_deadline = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    # In order not to retrieve winner every time.
    # Using a string instead of a class because class wasn't defined yet
    winner = models.ForeignKey(
        'LotteryParticipant', null=True,
        blank=True, related_name='lottery_winner', on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Lottery')
        verbose_name_plural = _('Lotteries')

    def __unicode__(self):
        return unicode('%s: %i' % (self.title, self.pk))

    def get_winner(self):
        """Returning the previously selected winner if exists,
        if not, select one and return it
        """
        if self.winner is not None:
            return self.winner
        else:
            participants = LotteryParticipant.objects.filter(lottery=self)
            if participants.count() > 0:
                winner = random.choice(list(participants))
                winner.is_winner = True
                winner.save()
                winner = LotteryParticipant.objects.get(
                    is_winner=True, lottery=self)
                self.winner = winner
                self.save()
                return winner

    def is_active(self):
        """Determines if a lottery is still accepting applicants"""
        return self.active and self.registration_deadline > \
            datetime.datetime.now().replace(tzinfo=utc) and self.winner is None

    def get_url(self):
        """Returns either the registration url or the winner url"""
        if self.winner is None:
            return urlresolvers.reverse(
                'lotteryapp:registration_form', args=[self.hash_key])
        else:
            return urlresolvers.reverse(
                'lotteryapp:lottery_winner', args=[self.hash_key])


class LotteryParticipant(models.Model):
    """Lottery participants model"""
    hash_key = models.UUIDField(default=uuid.uuid4, editable=False)
    lottery = models.ForeignKey(Lottery)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    entry_code = models.CharField(max_length=10, blank=True)
    is_winner = models.BooleanField(default=False)
    registerd = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Lottery Participant')
        verbose_name_plural = _('Lottery Participants')
        unique_together = ('email', 'entry_code')

    def __unicode__(self):
        return unicode('%s %s: %s' % (
            self.first_name, self.last_name, self.lottery))

    def save(self, *args, **kwargs):
        """Extra functionalities before saving participant.
        Note: will not execute in case of pulk insert
        """
        # Raising exception in case participant is set as a winner
        # and lottery already has a winnder
        if self.is_winner and type(self).objects.filter(
                lottery=self.lottery, is_winner=True).count() > 1:
            raise IntegrityError(
                'Lottery %s already has a winner' % self.lottery)

        # Creates a random base36 entry code of 10 digits
        # possibility of collision = 1/36^10 => almost 0
        if self.entry_code is None or self.entry_code == '':
            self.entry_code = random_base36_string(size=10)

        super(LotteryParticipant, self).save(*args, **kwargs)

    def validate_unique(self, exclude=None, *args, **kwargs):
        """extends validation on unique values to determine whether
        email already registerd for lottery or not
        """
        participants = LotteryParticipant.objects.filter(
            email=self.email, lottery=self.lottery)
        if participants.count() > 0 and self.id is None:
            raise ValidationError({
                'email': ['Email already exists for this lottery']})
        for participant in participants:
            if participant.id != self.id:
                raise ValidationError({
                    'email': ['Email already exists for this lottery']})

        super(LotteryParticipant, self).validate_unique(
            exclude=exclude, *args, **kwargs)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
