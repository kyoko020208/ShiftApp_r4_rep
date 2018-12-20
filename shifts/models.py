from django.db import models
import datetime
from django.utils import timezone
from accounts.models import UserManager

class Schedule(models.Model):
    class Meta:
        db_table = 'schedule'
    user = models.ForeignKey(UserManager, on_delete=models.PROTECT)
    start_time = models.TimeField('start time', default=datetime.time(7,0,0))
    end_time = models.TimeField('end time', default=datetime.time(7,0,0))
    date = models.DateField('date', default=timezone.now)
    created_at = models.DateField('date modified', default=timezone.now)

    def __str__(self):
        return self.date


class Availability(models.Model):
    class Meta:
        db_table = 'availability'
    user = models.ForeignKey(UserManager, on_delete=models.PROTECT)
    available = models.IntegerField('available', default=1)
    start_time = models.TimeField('start time', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('end time', default=datetime.time(7, 0, 0))
    date = models.DateField('date', default=timezone.now)
    created_at = models.DateField('date modified', default=timezone.now)

    def __str__(self):
        return self.available