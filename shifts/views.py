from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
import calendar
from collections import deque
from shifts.models import Schedule, Availability
from django.views.generic import ListView, FormView, DeleteView
from django.contrib import messages
from .forms import ShiftAddForm, AvailabilityAddForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from datetime import datetime
from django.views import generic
import datetime


class BaseCalendarMixin:
    """Base class for all calendar"""
    #0:starting on Monday, 1: starting on Tuesday, 6: starting on Sunday
    first_weekday = 0
    week_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def setup(self):
        """Setup calendar
        create instance for calendar.Calendar class
        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """changeable the first day for a week"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names

class MonthCalendarMixin(BaseCalendarMixin):
    """Base class for monthly calendar"""

    @staticmethod
    def get_previous_month(date):
        """return previous month"""
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    @staticmethod
    def get_next_month(date):
        """return next month"""
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """return all days in the month"""
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self):
        """return current month"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        """return monthly calendar dictionary"""
        self.setup()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'days': self.get_month_days(current_month),
            'current': current_month,
            'previous': self.get_previous_month(current_month),
            'next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data


class WeekCalendarMixin(BaseCalendarMixin):
    """Base class for week calendar"""
    def get_week_days(self):
        #return all days in a week
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today().replace(day=1)
        #pickup the week
        for week in self._calendar.monthdatescalendar(date.year, date.month):
            #if date is founded, return the week
            if date in week:
                return week

    def get_week_calendar(self):
        """returns week calendar library"""
        self.setup()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'days': days,
            'previous':first - datetime.timedelta(days=7),
            'next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'first': first,
            'last': last,
        }
        return calendar_data

class WeekWithScheduleMixin(WeekCalendarMixin):
    """Edit shift in the week calendar"""
    model = Schedule
    date_field = 'date'
    order_field = 'start_time'

    def get_week_schedules(self, days):
        for day in days:
            lookup = {self.date_field: day}
            queryset = Schedule.objects.filter(**lookup)
            if self.order_field:
                queryset = queryset.order_by(self.order_field)
            yield queryset

    def get_week_calendar(self):
        calendar_data = super().get_week_calendar()
        schedules = self.get_week_schedules(calendar_data['days'])
        calendar_data['schedule_list'] = schedules
        return calendar_data

class WeekWithAvailabilityMixin(WeekCalendarMixin):
    model = Availability
    date_field = 'date'
    order_field = 'start_time'

    def get_week_availability(self, days):
        for day in days:
            lookup = {self.date_field: day}
            queryset = Availability.objects.filter(**lookup)
            if self.order_field:
                queryset = queryset.order_by(self.order_field)
            yield queryset

    def get_week_calendar(self):
        calendar_data = super().get_week_calendar()
        availabilities = self.get_week_availability(calendar_data['days'])
        calendar_data['availability_list'] = availabilities
        return calendar_data


class HomeView(WeekWithScheduleMixin, generic.TemplateView):
    template_name = 'shifts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['week'] = self.get_week_calendar()
        context['user'] = self.request.user
        return context


class ShiftAddView(FormView):
    form_class = ShiftAddForm
    template_name = 'shifts/shiftsadd.html'
    success_url = reverse_lazy('shifts:index')

    def get_form_kwargs(self):
        #kwargs=dictionary
        kwargs = super(ShiftAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = ShiftAddForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, 'shifts/shiftsadd.html', {'form': form})
        form.save(commit=True)
        messages.success(request, "change has been saved")
        return redirect('shifts:index')

# class ShiftDeleteView(DeleteView):
#     model = Schedule
#     success_url = reverse_lazy('shifts:index')
#
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

class AvailabilityHomeView(MonthCalendarMixin, WeekWithAvailabilityMixin, generic.TemplateView):
    """home view for availability input"""
    template_name = 'shifts/availability.html'
    success_url = reverse_lazy('shifts:availability')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week = self.get_week_calendar()
        context['week'] = week
        context['month'] = self.get_month_calendar()
        context['week_row'] = zip(
            week['week_names'],
            week['days'],
            week['availability_list']
        )
        context['user'] = self.request.user
        return context


class AvailabilityAddView(FormView):
    form_class = AvailabilityAddForm
    template_name = 'shifts/availabilityadd.html'
    success_url = reverse_lazy('shifts:availability')

    def get_form_kwargs(self):
        kwargs = super(AvailabilityAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = AvailabilityAddForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, 'shifts/availabilityadd.html', {'form': form})
        availability_save = form.save(commit=False)
        availability_save.save()
        return redirect('shifts:availability')
