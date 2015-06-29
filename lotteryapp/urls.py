# django imports
from django.conf.urls import url

# local imports
from lotteryapp.views import Registration, ParticipantEntryCode, \
    LotteryWinner, LotteryList


urlpatterns = [
    url(r'^$', LotteryList.as_view(), name='home'),
    url(
        r'^registeration/(?P<lottery_hash_key>[A-Za-z0-9-]+)/$',
        Registration.as_view(), name='registration_form'),
    url(
        r'^participant/(?P<participant_hash_key>[A-Za-z0-9-]+)/code/$',
        ParticipantEntryCode.as_view(), name='participant_code'),
    url(
        r'^winner/(?P<lottery_hash_key>[A-Za-z0-9-]+)/$',
        LotteryWinner.as_view(), name='lottery_winner')
]
