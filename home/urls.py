from django.urls import path

from . import views


app_name = 'home'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('legal_notice', views.LegalNotice.as_view(), name='legal_notice'),
]
