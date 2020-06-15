from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='django_login'),
    path('logout/', LogoutView.as_view(), name='django_logout'),

]