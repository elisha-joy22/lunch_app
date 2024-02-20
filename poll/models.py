from django.db import models
from accounts.models import CustomUser
import datetime

# Create your models here.
class PollManager(models.Manager):
    def active_polls(self):
        return self.filter(end_date_time__gte=datetime.now())

    def is_poll_expired(self,ts):
        poll = self.get(ts=ts)
        return poll.end_date_time <= datetime.now()

    def get_poll_count(self,ts):
        return self.get(ts=ts).users.count()
    
    def get_polled_users(self,ts):
        poll = self.get(ts=ts)
        users_list = list(poll.users.all())
        return users_list


class Poll(models.Model):
    start_date_time = models.DateTimeField()
    end_date_time = models.DateField()
    event_date_time = models.DateField()
    poll_text = models.CharField(max_length=255)
    ts = models.CharField(max_length=255, default=None)
    channel_id = models.CharField(max_length=255)
    users = models.ManyToManyField(CustomUser, through='PollUser', related_name='polls')
    poll_closed = models.BooleanField(default=False)

    objects = PollManager()

    def __str__(self):
        return self.poll_text


class PollUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)    