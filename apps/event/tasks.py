from celery.utils.log import get_task_logger
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from test1.celery import app
from apps.event.models import Event
from tools.email_notification import send_mail_notification

logger = get_task_logger(__name__)
EMAIL_SUBJECT = 'New Task Notification'


@app.task(name='notification')
def check_time_to_notify():
    now = timezone.now()
    previous_call = now - relativedelta(minutes=1)
    for event in Event.objects.filter(notification_time__gte=previous_call, notification_time__lte=now):
        send_mail_notification(EMAIL_SUBJECT, event)
        logger.info(f"Emails were sent to recipients of the {event.title}")
