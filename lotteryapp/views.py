# stdlib imports
import datetime

# django imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core import urlresolvers
from django.utils.timezone import utc
from django.db.models import Q

# local imports
from lotteryapp.models import Lottery, LotteryParticipant
from lotteryapp.forms import ParticipantRegistrationForm


class LotteryList(View):
    """List of all lotteries in the system"""

    template = 'lotteryapp/lottery-list.html'

    def get_context_data(self):
        """Generating base context data"""
        return {
            'active_lotteries': Lottery.objects.filter(
                winner__isnull=True,
                registration_deadline__gt=
                datetime.datetime.now().replace(tzinfo=utc)),
            'inactive_lotteries': Lottery.objects.filter(
                Q(winner__isnull=False) | Q(
                    registration_deadline__lte=
                    datetime.datetime.now().replace(tzinfo=utc)))}

    def get(self, request, *args, **kwargs):
        """GET http method"""
        return render(request, self.template, self.get_context_data())


class Registration(View):
    """Registration form view/validation/saving"""

    form_class = ParticipantRegistrationForm
    template = 'lotteryapp/registration.html'

    def get_context_data(self):
        """Generating base context data"""
        lottery = get_object_or_404(
            Lottery, hash_key=self.kwargs['lottery_hash_key'])

        return {
            'lottery': lottery,
            'lottery_deadline': lottery.registration_deadline.strftime(
                '%A %B %-d, %Y, at %-I:%M %p UTC'),
            'form': self.form_class(initial={'lottery': lottery})}

    def get(self, request, *args, **kwargs):
        """GET http method"""
        context = self.get_context_data()
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        """POST http method"""
        context = self.get_context_data()
        form = self.form_class(request.POST)
        context['form'] = form
        if form.is_valid() and context['lottery'].is_active():
            result = form.save()
            url = urlresolvers.reverse(
                'lotteryapp:participant_code', args=[result.hash_key])
            return HttpResponseRedirect(url)
        return render(request, self.template, context)


class ParticipantEntryCode(View):
    """Registeration confirmation page, with participation entry code"""

    template = 'lotteryapp/participant-entry-code.html'

    def get_context_data(self):
        """Generating base context data"""
        participant = get_object_or_404(
            LotteryParticipant, hash_key=self.kwargs['participant_hash_key'])
        return {
            'participant': participant,
            'lottery_deadline':
            participant.lottery.registration_deadline.strftime(
                '%A %B %-d, %Y, at %-I:%M %p UTC')}

    def get(self, request, *args, **kwargs):
        """GET http method"""
        return render(request, self.template, self.get_context_data())


class LotteryWinner(View):
    """View the winner of a certain lottery"""

    template = 'lotteryapp/lottery-winner.html'

    def get_context_data(self):
        """Generating base context data"""
        lottery = get_object_or_404(
            Lottery, hash_key=self.kwargs['lottery_hash_key'])
        winner = None
        try:
            winner = LotteryParticipant.objects.get(
                lottery=lottery, is_winner=True)
        except LotteryParticipant.DoesNotExist:
            pass
        return {
            'lotter': lottery,
            'winner': winner,
            'lottery_deadline': lottery.registration_deadline.strftime(
                '%A %B %-d, %Y, at %-I:%M %p UTC')}

    def get(self, request, *args, **kwargs):
        """GET http method"""
        return render(request, self.template, self.get_context_data())
