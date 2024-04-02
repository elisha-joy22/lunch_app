from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .models import ScheduledPoll
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

@receiver(post_save, sender=ScheduledPoll)
def create_schedule_on_poll_creation(sender, instance, created, **kwargs):
    days_until_event_after_poll = instance.days_until_event_after_poll
    poll_end_time = instance.poll_end_time
    event_time = instance.event_time
    poll_text = instance.poll_text
    args = (poll_end_time, event_time, poll_text, days_until_event_after_poll)

    if created:
        print("if")
        crontab_instance = CrontabSchedule.objects.get(id=instance.crontab.id)
        periodic_task = PeriodicTask.objects.create(
            crontab=crontab_instance,
            name=instance.name,
            task='poll.tasks.create_scheduled_poll',
            args=json.dumps([str(poll_end_time), str(event_time), poll_text, str(days_until_event_after_poll)])
        )
        instance.periodic_task_id = periodic_task.id
        instance.periodic_task.enable = True
        instance.save()
    else:
        print("else")
        periodic_task_obj = instance.periodic_task
        periodic_task_obj.name = instance.name
        periodic_task_obj.args = json.dumps([str(poll_end_time), str(event_time), poll_text, str(days_until_event_after_poll)])
        periodic_task_obj.save()

@receiver(post_delete, sender=ScheduledPoll)
def delete_scheduled_poll(sender, instance, **kwargs):
    if instance.periodic_task:
        instance.periodic_task.delete()