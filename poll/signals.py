from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .models import ScheduledPoll,Poll
from django_celery_beat.models import PeriodicTask, CrontabSchedule, ClockedSchedule
import json

@receiver(post_save, sender=ScheduledPoll)
def create_cron_schedule_on_poll_creation(sender, instance, created, **kwargs):
    days_until_event_after_poll = instance.days_until_event_after_poll
    poll_end_time = instance.poll_end_time
    event_time = instance.event_time
    poll_text = instance.poll_text
    args = (poll_end_time, event_time, poll_text, days_until_event_after_poll)

    if created:
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
        periodic_task_obj = instance.periodic_task
        periodic_task_obj.name = instance.name
        periodic_task_obj.args = json.dumps([str(poll_end_time), str(event_time), poll_text, str(days_until_event_after_poll)])
        periodic_task_obj.save()


@receiver(post_delete, sender=ScheduledPoll)
def delete_scheduled_poll(sender, instance, **kwargs):
    if instance.periodic_task:
        instance.periodic_task.delete()



@receiver(post_save, sender=Poll)
def create_clock_schedule_on_poll_creation(sender, instance, created, **kwargs):

    if created:
        clocked_schedule_instance = ClockedSchedule.objects.create(
            clocked_time=instance.end_date_time,
        )
        instance.clocked_schedule = clocked_schedule_instance

        periodic_task = PeriodicTask.objects.create(
            clocked=clocked_schedule_instance,
            name=instance.poll_text + str(instance.event_date_time),
            one_off = True,
            task='poll.tasks.send_poll_details_via_slack',
            args=json.dumps([str(instance.id)])
        )
        instance.periodic_task_id = periodic_task.id
        instance.periodic_task.enabled = True
        instance.save()

    else:
        clocked_schedule_obj = instance.clocked_schedule
        clocked_schedule_obj.clocked_time = instance.end_date_time
        clocked_schedule_obj.save()

        periodic_task_obj = instance.periodic_task
        periodic_task_obj.args = json.dumps([str(instance.id)])
        periodic_task_obj.enabled = True
        periodic_task_obj.save()



@receiver(post_delete, sender=Poll)
def delete_poll(sender, instance, **kwargs):
    if instance.periodic_task:
        instance.periodic_task.delete()
    if instance.clocked_schedule:
        instance.clocked_schedule.delete()
