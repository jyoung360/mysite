from django.urls import path

from . import views

urlpatterns = [
    path('device/<int:id>', views.index, name='index'),
]