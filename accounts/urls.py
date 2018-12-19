
from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns=[
    path('before_signup/', views.ManagerStatusView.as_view(), name='before_signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/<int:is_manager>', views.SignUpView.as_view(), name='signup'),
]