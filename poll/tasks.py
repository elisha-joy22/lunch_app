from celery import shared_task
from slack_sdk.errors import SlackApiError
from datetime import datetime, timedelta, timezone
import pytz
import os

from poll.models import Poll
from poll.slack_init import slack_app

channel_id = os.getenv("LUNCH_CHANNEL_ID")

@shared_task
def create_scheduled_poll(start_time,end_time, event_time, poll_text, days_until_event_after_poll=None):
    try:
        kolkata_timezone = pytz.timezone('Asia/Kolkata')
        date_time_now = datetime.now(timezone.utc).astimezone(kolkata_timezone)
        start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time, '%H:%M:%S').time()
        event_time = datetime.strptime(event_time, '%H:%M:%S').time()
        days_until_event_after_poll = int(days_until_event_after_poll)
        
        start_date_time = date_time_now.replace(hour=start_time.hour, minute=start_time.minute) 
        end_date_time = date_time_now.replace(hour=end_time.hour, minute=end_time.minute)
        event_date_time = (date_time_now.replace(hour=event_time.hour, minute=event_time.minute) + timedelta(days=days_until_event_after_poll)).replace(tzinfo=None)
    

        Poll.objects.create(
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            event_date_time=event_date_time,
            poll_text=poll_text
        )
        print("Poll creation success")
    except Exception as e:
        print("Creating poll failed:", e)



@shared_task
def send_poll_details_via_slack(poll_id):
    print("poll_id",poll_id)
    poll_instance = Poll.objects.get(id=poll_id)
    poll_instance.is_active = False
    poll_instance.save()

    end_date_time = poll_instance.end_date_time
    event_date_time_str = str(poll_instance.event_date_time)
    
    event_date_time = datetime.fromisoformat(event_date_time_str)

    # Add 5 hours and 30 minutes
    new_event_date_time = event_date_time + timedelta(hours=5, minutes=30)

    # Format the new datetime as a string
    formatted_new_event_date_time = new_event_date_time.strftime('%Y-%m-%d %H:%M:%S')

    poll_text = poll_instance.poll_text

    count = Poll.objects.get_poll_count(id=poll_instance.id) or 0
    extra_counts = Poll.objects.get_poll_extra_count(id=poll_instance.id) or 0
    slack_message_text1 = f"The poll has ended just now!\n {poll_text}\n Event Date:{formatted_new_event_date_time}\n"
    slack_message_text2 = f"Count:{count}\n Extra_counts:{extra_counts}\n Total Count:{count + extra_counts}"
    slack_message = slack_message_text1 + slack_message_text2

    try:
        response = slack_app.client.chat_postMessage(
            channel=channel_id,
            text=slack_message,
        )
        print("successfully posted to slack\nresponse:",{response})
        return response
    except SlackApiError as e:
        print(f"Error posting content: {e.response['error']}")



    