# django imports
from django.contrib import admin
from django.core import urlresolvers

# local imports
from lotteryapp.models import Lottery, LotteryParticipant


def draw_winner(modeladmin, request, queryset):
    """Admin group action to draw winner of a lottery"""
    for lottery in queryset:
        lottery.get_winner()
draw_winner.short_description = 'Draw Winner for Lotteries'


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    """Admin panel definition for Lottery model."""

    list_display = (
        'id', 'title', 'created', 'registration_deadline',
        'active', 'lottery_winner')
    search_fields = ['title']
    raw_id_fields = ['winner']
    actions = [draw_winner]

    def lottery_winner(self, obj):
        """returns a url for the winner of the lottery in the admin"""
        if obj.winner is not None:
            return '<a href="%s"> %s </a>' % (
                urlresolvers.reverse(
                    'admin:lotteryapp_lotteryparticipant_change',
                    args=[obj.winner.pk]), obj.winner)
        return None
    lottery_winner.allow_tags = True


@admin.register(LotteryParticipant)
class LotteryParticipantAdmin(admin.ModelAdmin):
    """Admin panel definition for LotteryParticipant model."""

    list_display = (
        'id', 'full_name', 'registerd', 'lottery',
        'email', 'is_winner', 'entry_code')
    search_fields = ['first_name', 'last_name', 'entry_code', 'email']
    list_filter = ['lottery', 'is_winner']
    raw_id_fields = ['lottery']
