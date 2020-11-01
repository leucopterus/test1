from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_mail_notification(subject, event):
    recipient_list = [event.organizer.email,]
    recipient_list.extend(event.participators.all().values_list('email', flat=True))
    message = render_to_string(
        'event/notification_email.html',
        {
            'title': event.title,
            'description': event.description,
            'place': event.place,
            'organizer': event.organizer,
            'participators': event.participators.all,
            'created': event.created,
            'start_date': event.start_date
        }
    )
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, '', email_from, recipient_list, html_message=message)
