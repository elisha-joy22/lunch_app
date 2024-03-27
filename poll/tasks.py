from celery import shared_task
from datetime import datetime,timedelta,timezone
import pytz

from poll.models import Poll



@shared_task
def create_scheduled_poll(end_time,event_time,poll_text,days_until_event_after_poll=None):
    print("inside create")
    utc_now = datetime.now(timezone.utc)
    kolkata_timezone = pytz.timezone('Asia/Kolkata')
    start_date_time = utc_now.astimezone(kolkata_timezone)
    
    end_time = datetime.strptime(end_time,'%H:%M:%S')
    event_time = datetime.strptime(event_time,'%H:%M:%S')
    days_until_event_after_poll = int(days_until_event_after_poll)
    print("start",start_date_time)
    print("end",end_time)
    print("event",event_time)

    try:
        Poll.objects.create(
            start_date_time = start_date_time,
            end_date_time = start_date_time.replace(hour=end_time.hour, minute=end_time.minute),
            event_date_time = start_date_time.replace(hour=event_time.hour, minute=event_time.minute) + timedelta(days=days_until_event_after_poll),
            poll_text = poll_text
        )
        print("Poll creation success")
    except Exception as e:
        print("creating poll failed!!")
        print(e)



