# django imports
from django import forms

# local imports
from lotteryapp.models import LotteryParticipant


class ParticipantRegistrationForm(forms.ModelForm):
    """ModelForm for lottery participants registration"""

    class Meta:
        model = LotteryParticipant
        exclude = ['registerd', 'hash_key', 'entry_code', 'is_winner']

    def __init__(self, *args, **kwargs):
        """initializing ParticipantRegistrationForm"""
        super(ParticipantRegistrationForm, self).__init__(*args, **kwargs)

        # extending custom fields
        self.fields['lottery'].widget = forms.widgets.HiddenInput()
        # adding css class to fields.
        # TODO: Not sure adding css in the logic. Didn't find another way
        for field in self.fields.iterkeys():
            self.fields[field].widget.attrs['class'] = 'form-control'
