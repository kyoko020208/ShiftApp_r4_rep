from rest_framework import routers
from . import api_views

from django.urls import path

router = routers.DefaultRouter()
router.register('users', api_views.UserViewSet)
router.register('schedule', api_views.ScheduleViewSet)
