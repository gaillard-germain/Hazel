from django.urls import path, include

from . import views


app_name = 'registration'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]
