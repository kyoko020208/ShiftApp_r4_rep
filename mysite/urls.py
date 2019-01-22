from django.contrib import admin
from django.urls import include, path
from shifts.api_urls import router as api_router

#from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shifts/', include('shifts.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include(api_router.urls)),
]