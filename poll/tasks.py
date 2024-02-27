import logging
from celery import shared_task
from datetime import datetime,timedelta
from poll.models import Poll


#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@shared_task
def create_scheduled_poll():
    start_date_time = datetime.now()
    try:
        Poll.objects.create(
            start_date_time = start_date_time,
            end_date_time = start_date_time.replace(hour=18, minute=30),
            event_date_time = start_date_time.replace(hour=12, minute=30) + timedelta(days=1),
            poll_text = "Please poll if you wanna join us for lunch!!"
        )
    except:
        print("creating poll failed!!")
    print("1 min")
