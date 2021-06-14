from django.urls import path, include

from . import views


app_name = 'registration'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout', views.logout_request, name='logout'),
    path('signup', views.signup, name='signup'),
    path('myaccount', views.manage_account, name='myaccount'),
    path('regchild_step1', views.regchild_step1, name='regchild_step1'),
    path('regchild_step2', views.regchild_step2, name='regchild_step2'),
    path('regchild_step3', views.regchild_step3, name='regchild_step3'),
    path('regchild_step4', views.regchild_step4, name='regchild_step4'),
]
