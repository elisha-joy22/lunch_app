from celery import shared_task
from datetime import datetime, timedelta, timezone
import pytz

from poll.models import Poll

@shared_task
def create_scheduled_poll(end_time, event_time, poll_text, days_until_event_after_poll=None):
    try:
        kolkata_timezone = pytz.timezone('Asia/Kolkata')
        start_date_time = datetime.now(timezone.utc).astimezone(kolkata_timezone)

        end_time = datetime.strptime(end_time, '%H:%M:%S').time()
        event_time = datetime.strptime(event_time, '%H:%M:%S').time()
        days_until_event_after_poll = int(days_until_event_after_poll)
        
        end_date_time = start_date_time.replace(hour=end_time.hour, minute=end_time.minute)
        event_date_time = (start_date_time.replace(hour=event_time.hour, minute=event_time.minute) + timedelta(days=days_until_event_after_poll)).replace(tzinfo=None)
    

        Poll.objects.create(
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            event_date_time=event_date_time,
            poll_text=poll_text
        )
        print("Poll creation success")
    except Exception as e:
        print("Creating poll failed:", e)
