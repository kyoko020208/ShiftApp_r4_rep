from django.db import models
import datetime
from django.utils import timezone
from accounts.models import UserManager

class Schedule(models.Model):
    class Meta:
        db_table = 'schedule'
    user = models.ForeignKey(UserManager, on_delete=models.PROTECT)
    schedule_id = models.AutoField(primary_key=True, unique=True)
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
    available = models.CharField('available', default=1, max_length=30)
    start_time = models.TimeField('start time', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('end time', default=datetime.time(7, 0, 0))
    date = models.DateField('date', default=timezone.now)
    created_at = models.DateField('date modified', default=timezone.now)

    def __str__(self):
        return self.available


class Shifts(models.Model):
    class Meta:
        db_table = 'shifts'
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    assigned_user = models.CharField('assgined_user', default="", max_length=30)
    created_at = models.DateField('date modified', default=timezone.now)

    def __str__(self):
        return self.assigned_user
