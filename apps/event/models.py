from django.db import models

from apps.base.models import User, IdAbstractModel, TimestampAbstractModel


class Event(IdAbstractModel, TimestampAbstractModel):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True)
    place = models.CharField(max_length=256)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    participators = models.ManyToManyField(User, related_name='events')
    start_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'
