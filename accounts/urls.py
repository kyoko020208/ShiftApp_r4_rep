
from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns=[
    #path('ChooseStatus/', views.ManagerStatusView.as_view(), name='Manager'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]