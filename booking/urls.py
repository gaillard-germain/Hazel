from django.urls import path, re_path

from . import views


app_name = 'booking'

urlpatterns = [
    path('select_child', views.SelectChild.as_view(), name='select_child'),
    re_path(r'^calendar/(?P<child_id>\d+)/$', views.Calendar.as_view(),
            name='calendar'),
    path('modify', views.Modify.as_view(), name='modify'),
]
