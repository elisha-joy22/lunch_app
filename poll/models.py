from django.db import models

import datetime

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
        return users_list


class Poll(models.Model):
    start_date_time = models.DateTimeField()
    end_date_time = models.DateField()
    event_date_time = models.DateField()
    poll_text = models.CharField(max_length=255)
    users = models.ManyToManyField(CustomUser, through='PollUser', related_name='polls')
    is_active = models.BooleanField(default=True)

    objects = PollManager()

    def __str__(self):
        return self.poll_text


class PollUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)    