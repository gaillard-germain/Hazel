from django.urls import path, include

from . import views


app_name = 'registration'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout', views.logout_request, name='logout'),
    path('signup', views.signup, name='signup'),
    path('myaccount', views.manage_account, name='myaccount'),
    path('regchild', views.register_new_child, name='regchild'),
]
