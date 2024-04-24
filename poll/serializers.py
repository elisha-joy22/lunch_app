from rest_framework import serializers
from poll.models import Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'start_date_time', 'end_date_time', 'event_date_time', 'poll_text', 'is_active', 'users']

    