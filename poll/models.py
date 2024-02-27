from django.db import models
import datetime
from django.utils import timezone

from accounts.models import CustomUser


# Create your models here.
class PollManager(models.Manager):
    def active_polls(self):
        return self.filter(is_active=True)

    def is_poll_expired(self,id):
        poll = self.get(pk=id)
        return poll.end_date_time <= datetime.now()

    def get_poll_count(self,id):
        return self.get(pk=id).users.count()
    
    def get_polled_users(self,id):
        poll = self.get(pk=id)
        users_list = list(poll.users.all())
        print("users_list",users_list)
        return users_list


class Poll(models.Model):
    start_date_time = models.DateTimeField(default=timezone.now)
    end_date_time = models.DateTimeField(default=timezone.now)
    event_date_time = models.DateTimeField(default=timezone.now)
    poll_text = models.CharField(max_length=255)
    users = models.ManyToManyField(CustomUser, through='PollUser', related_name='polls')
    is_active = models.BooleanField(default=True)

    objects = PollManager()

    def __str__(self):
        return self.poll_text


class PollUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)    