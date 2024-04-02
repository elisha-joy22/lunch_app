from django.db import models
from datetime import time
from pytz import timezone as tz
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule,PeriodicTask
from django.db.models import Q

from accounts.models import CustomUser


# Create your models here.
class PollManager(models.Manager):
    def active_polls(self):
        ist = tz('Asia/Kolkata') 
        current_time = timezone.now().astimezone(ist)
        print(current_time)
        return self.filter(Q(is_active=True) & Q(end_date_time__gte=current_time))
    
    def expired_polls(self,id):
        return self.filter(end_date_time__lte=timezone.now())

    def get_poll_count(self,id):
        return self.get(pk=id).users.count()
    
    def get_polled_users(self,id):
        return self.get(pk=id).users.all()
        


class Poll(models.Model):
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    event_date_time = models.DateTimeField()
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
    name = models.CharField(max_length=255)
    poll_start_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    poll_end_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    event_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    days_until_event_after_poll = models.PositiveIntegerField()
    poll_text = models.CharField(max_length=255)
    
    crontab = models.ForeignKey(CrontabSchedule,on_delete=models.CASCADE)
    periodic_task = models.OneToOneField(PeriodicTask,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.name    