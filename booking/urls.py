from django.urls import path

from . import views


app_name = 'booking'

urlpatterns = [
    path('calendar', views.Calendar.as_view(), name='calendar'),
]
