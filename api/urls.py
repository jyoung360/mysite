from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('device/<int:id>', views.device, name='device'),
    path('devices', views.listDevices, name='list-devices'),
]