from django.urls import path
from shifts.views import mobileapp


app_name = 'shifts'

urlpatterns=[
    path('index/', mobileapp.HomeView.as_view(), name='index'),
    path('index/<int:year>/<int:month>/<int:day>/', mobileapp.HomeView.as_view(), name='index'),
    path('index/shiftsadd/', mobileapp.ShiftAddView.as_view(), name='shiftsadd'),
    path('availability/', mobileapp.AvailabilityHomeView.as_view(), name='availability'),
    path('availability/<int:year>/<int:month>/', mobileapp.AvailabilityHomeView.as_view(), name='availability'),
    path('availability/<int:year>/<int:month>/<int:day>/', mobileapp.AvailabilityHomeView.as_view(), name='availability'),
    path('availability/add/', mobileapp.AvailabilityAddView.as_view(), name='availabilityadd'),
    path('availability/add/<int:month>/<int:day>/', mobileapp.AvailabilityAddView.as_view(), name='availabilityadd'),
    path('assign/', mobileapp.ShiftsAssignView.as_view(), name='assign'),
    path('assign/<int:schedule_id>/', mobileapp.ShiftsAssignView.as_view(), name='assign'),
]