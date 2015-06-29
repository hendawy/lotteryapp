# stdlib imports
import datetime

# django imports
from django.test import TestCase
from django.utils.timezone import utc

# local imports
from lotteryapp.models import Lottery, LotteryParticipant


class LotteryTestCase(TestCase):
    """Test cases for Lottery Model.
    TEST SCOPE:
        - test_get_winner_found_winner()
        - test_get_winner_draw_winner()
        - test_get_winner_draw_winner_no_participants()
        - test_is_active_inactive_winner_found()
        - test_is_active_inactive_deadline_reached()
        - test_is_active_inactive_active_false()
        - test_is_active_active()

    Total test cases: 7
    """

    def setUp(self):
        self.lottery = Lottery.objects.create(
            title='testing lottery',
            registration_deadline=
            datetime.datetime.now().replace(tzinfo=utc) +
            datetime.timedelta(days=20))
        self.participant1 = LotteryParticipant.objects.create(
            first_name='Mohamed',
            last_name='Ibrahim',
            email='ibrahim@email.com',
            lottery=self.lottery)
        self.participant2 = LotteryParticipant.objects.create(
            first_name='Mohamed',
            last_name='Fathy',
            email='fathy@email.com',
            lottery=self.lottery)
        self.participant3 = LotteryParticipant.objects.create(
            first_name='Mohamed',
            last_name='Hendawy',
            email='hendawy@email.com',
            lottery=self.lottery)
        self.lottery.winner = self.participant1
        self.lottery.save()

    def test_get_winner_found_winner(self):
        """Testing getting a winner already drawn"""

        lottery = Lottery.objects.get(title='testing lottery')
        self.assertNotEqual(lottery.winner, None)
        winner = lottery.get_winner()
        self.assertEqual(winner, self.participant1)
        self.assertEqual(winner, lottery.winner)

    def test_get_winner_draw_winner(self):
        """Testing drawing a random winner"""

        lottery = Lottery.objects.get(title='testing lottery')
        winner = lottery.get_winner()
        self.assertNotEqual(lottery.winner, None)
        lottery = Lottery.objects.get(title='testing lottery')
        self.assertEqual(winner, lottery.winner)

    def test_get_winner_draw_winner_no_participants(self):
        """Testing drawing a random winner where lottery has no participants"""

        self.participant1.delete()
        self.participant2.delete()
        self.participant3.delete()
        lottery = Lottery.objects.get(title='testing lottery')
        lottery.get_winner()
        lottery = Lottery.objects.get(title='testing lottery')
        self.assertEqual(lottery.winner, None)

    def test_is_active_inactive_winner_found(self):
        """Testing lottery inactivity due to finding a winner"""
        lottery = Lottery.objects.get(title='testing lottery')
        self.assertFalse(lottery.is_active())

    def test_is_active_inactive_deadline_reached(self):
        """Testing lottery inactivity because of reachign deadline"""
        lottery = Lottery.objects.get(title='testing lottery')
        lottery.winner = None
        lottery.registration_deadline = \
            datetime.datetime.now().replace(tzinfo=utc) - \
            datetime.timedelta(days=20)
        lottery.save()
        lottery = Lottery.objects.get(title='testing lottery')
        self.assertFalse(lottery.is_active())

    def test_is_active_inactive_active_false(self):
        """Testing lottery inactivity because of flaging inactive"""
        lottery = Lottery.objects.get(title='testing lottery')
        lottery.winner = None
        lottery.active = False
        lottery.save()
        lottery = Lottery.objects.get(title='testing lottery')
        self.assertFalse(lottery.is_active())

    def test_is_active_active(self):
        """Testing lottery inactivity because of flaging inactive"""
        lottery = Lottery.objects.get(title='testing lottery')
        lottery.winner = None
        lottery.save()
        lottery = Lottery.objects.get(title='testing lottery')
        self.assertTrue(lottery.is_active())
