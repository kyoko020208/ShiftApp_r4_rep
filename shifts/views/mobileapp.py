from django.views.generic import FormView
from django.contrib import messages
from shifts.forms import ShiftAddForm, AvailabilityAddForm, ShiftAssignForm
from .calendar import WeekWithScheduleMixin, MonthCalendarMixin, WeekWithAvailabilityMixin
from django.urls import reverse_lazy
from datetime import datetime
from django.views import generic
import datetime
from django.shortcuts import render, redirect
from accounts.models import UserManager
from shifts.models import Availability, Schedule



class HomeView(WeekWithScheduleMixin, WeekWithAvailabilityMixin, generic.TemplateView):
    template_name = 'shifts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['week'] = self.get_week_calendar()
        context['user'] = self.request.user
        week = self.get_week_calendar()
        context['week_row'] = zip(
            week['week_names'],
            week['days'],
            week['schedule_list'],
            week['availability_list']
        )
        context['username'] = UserManager.objects.values_list('username', flat=True)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week = self.get_week_calendar()
        context['week'] = self.get_week_calendar()
        context['month'] = self.get_month_calendar()
        context['week_row'] = zip(
            week['week_names'],
            week['days'],
            week['availability_list'],
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

class ShiftsAssignView(FormView):
    form_class = ShiftAssignForm
    template_name = 'shifts/shiftsAssign.html'
    success_url = reverse_lazy('shifts:assign')

    def get_form_kwargs(self):
        kwargs = super(ShiftsAssignView, self).get_form_kwargs()
        kwargs['schedule'] = self.kwargs.get('schedule_id')
        return kwargs

    def get_suggestion(self):
        queryset = Schedule.objects

    def post(self, request, *args, **kwargs):
        form = ShiftAssignForm(request.POST, schedule=self.kwargs.get('schedule_id'))
        if not form.is_valid():
            return render(request, 'shifts/shiftsAssign.html', {'form': form, 'schedule':self.kwargs.get('schedule_id')})
        shifts_save = form.save(commit=False)
        shifts_save.save()
        return redirect('shifts:index')

