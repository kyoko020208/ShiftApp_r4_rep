from django import forms
from shifts.models import Schedule, Availability, Shifts
from accounts.models import UserManager
from django.utils import timezone
from accounts.models import UserManager
from . import models


class ShiftAddForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('start_time', 'end_time', 'date',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ShiftAddForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs = {'placeholder': 'Start time'}
        self.fields['start_time'].auto_focus = True
        self.fields['end_time'].widget.attrs = {'placeholder': 'End Time'}
        self.fields['end_time'].auto_focus = True
        #self.fields['date'].widget.attrs = {'placeholder': 'timezone.now'}

    def save(self, commit=True):
        shift_info = super(ShiftAddForm, self).save(commit=False)
        shift_info.user = self._user
        if commit:
            shift_info.save()
        return shift_info


class AvailabilityAddForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ('start_time', 'end_time', 'available', 'date', )


    def __init__(self, *args, **kwargs):
        CHOICE = {
            ('0', 'OK'),
            ('1', 'NG'),
        }
        self._user = kwargs.pop('user')
        super(AvailabilityAddForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs = {'placeholder': 'Start time'}
        self.fields['start_time'].auto_focus = True
        self.fields['end_time'].widget.attrs = {'placeholder': 'End Time'}
        self.fields['end_time'].auto_focus = True
        #self.fields['date'].required = True
        self.fields['date'].widget.attrs = {'placeholder': 'timezone.now'}
        self.fields['available'] = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICE)

    def clean(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        available = self.cleaned_data['available']

        if start_time > end_time:
            raise forms.ValidationError('start time must be earlier than end time')


    def save(self, commit=True):
        availability_info = super(AvailabilityAddForm, self).save(commit=False)
        availability_info.user = self._user
        if commit:
            availability_info.save()
            # UserManager.objects.create(user=user_info)

        return availability_info


class ShiftAssignForm(forms.ModelForm):

    class Meta:
        model = Shifts
        fields = {'assigned_user', }

    def __init__(self, *args, **kwargs):
        first_name_group = UserManager.objects.values_list('first_name', flat=True)
        user_id_group = UserManager.objects.values_list('user_id', flat=True)
        CHOICE = []
        for value, key in zip(first_name_group, user_id_group):
             CHOICE.append((key, value))
        self._shift = kwargs.pop('shift')
        super(ShiftAssignForm, self).__init__(*args, **kwargs)
        self.fields['assigned_user'] = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICE)

    def save(self, commit=True):
        shiftsassign = super(ShiftAssignForm, self).save(commit=False)
        shiftsassign.shift = self._shift
        if commit:
            shiftsassign.save()

        return shiftsassign
