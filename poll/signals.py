from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django_celery_beat.models import CrontabSchedule,PeriodicTask
import json

from poll.models import ScheduledPoll



# Define the signal handler function
@receiver(post_save, sender=ScheduledPoll)
def create_schedule_on_poll_creation(sender, instance, created, **kwargs):
    if created: 
        days_until_event_after_poll = instance.days_until_event_after_poll
        poll_end_time = instance.poll_end_time
        event_time = instance.event_time
        poll_text = instance.poll_text
        args = (poll_end_time,event_time,poll_text,days_until_event_after_poll,)

        crontab_instance = CrontabSchedule.objects.get(id=instance.crontab.id)

        periodic_task = PeriodicTask.objects.create(
            crontab=crontab_instance,
            name=instance.name,
            task='lunch_app.tasks.create_scheduled_poll',
            args=json.dumps([str(poll_end_time),str(event_time),poll_text,str(days_until_event_after_poll),])
        )
        instance.periodic_task = periodic_task
        instance.periodic_task.enable = True
        instance.save()

    else:
        print("else")
        days_until_event_after_poll = instance.days_until_event_after_poll
        poll_end_time = instance.poll_end_time
        event_time = instance.event_time
        poll_text = instance.poll_text
    
        periodic_task_obj = PeriodicTask.objects.get(id=instance.periodic_task.id)
        periodic_task_obj.name=instance.name,
        periodic_task_obj.args=json.dumps([str(poll_end_time),str(event_time),poll_text,str(days_until_event_after_poll),])
        periodic_task_obj.save()
        print(periodic_task_obj)
