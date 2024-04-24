from typing import Any
from django import forms
from poll.models import Poll,ScheduledPoll,PollExtraCount

class CreatePollForm(forms.ModelForm):
    start_date_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    event_date_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = Poll
        fields = ['start_date_time', 'end_date_time', 'event_date_time', 'poll_text']

    
    def clean(self):
        cleaned_data = super().clean()
        start_date_time = cleaned_data.get('start_date_time')
        end_date_time = cleaned_data.get('end_date_time')
        event_date_time = cleaned_data.get('event_date_time')

        if start_date_time and end_date_time and event_date_time:
            if start_date_time >= end_date_time:
                self.add_error('end_date_time', 'End date/time must be greater than start date/time.')
            if end_date_time >= event_date_time:
                self.add_error('event_date_time', 'Event date/time must be greater than end date/time.')



class PollResponseForm(forms.ModelForm):
    response = forms.ChoiceField(choices=[(True,'Yes'),(False,'No')], widget=forms.RadioSelect)

    class Meta:
        model = Poll
        fields = []

class PollExtraCountForm(forms.ModelForm):
    class Meta:
        model = PollExtraCount
        fields = ["department","count"]


class ScheduledPollForm(forms.ModelForm):
    class Meta:
        model = ScheduledPoll
        fields = ['name','poll_start_time','poll_end_time','event_time','days_until_event_after_poll','poll_text','crontab']
        widgets = {
            'poll_start_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'poll_end_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'event_time': forms.TimeInput(attrs={'class': 'timepicker'})
        }
