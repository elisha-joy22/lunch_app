from django.db import models
from datetime import time
import datetime
from django.utils import timezone
from multiselectfield import MultiSelectField
from django_celery_beat.models import CrontabSchedule,PeriodicTask

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


class ScheduledPoll(models.Model):
    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    name = models.CharField(max_length=255)
    poll_start_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    poll_end_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    event_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    days_until_event_after_poll = models.PositiveIntegerField()
    poll_text = models.CharField(max_length=255)
    
    crontab = models.ForeignKey(CrontabSchedule,on_delete=models.CASCADE)
    periodic_task = models.ForeignKey(PeriodicTask,on_delete=models.CASCADE,null=True)
    
    #cron_start_date_time = models.DateTimeField(default=timezone.now().replace(hour=0, minute=0, second=0))
    #cron_days_of_week = MultiSelectField(max_length=30, choices=DAY_CHOICES)


    def __str__(self):
        return self.name    