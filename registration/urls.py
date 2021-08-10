from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LegalGuardianForm


app_name = 'registration'

urlpatterns = [
    path(
        'login',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='registration/logout.html'
        ),
        name='logout'
    ),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('regfamily', views.RegFamily.as_view(), name='regfamily'),
    path('myaccount', views.ManageAccount.as_view(), name='myaccount'),
    re_path(
        '^regchild_step1\/?(?P<child_id>\d+)?\/?',
        views.RegChild.as_view(),
        name='regchild_step1'
    ),
    re_path(
        '^regchild_step2\/?(?P<child_id>\d+)?\/?',
        views.RegChild.as_view(
            form_class=LegalGuardianForm,
            session_key='lg1',
            title='Mère / Responsable Légal 1',
            step=2
        ),
        name='regchild_step2'
    ),
    re_path(
        '^regchild_step3\/?(?P<child_id>\d+)?\/?',
        views.RegChild.as_view(
            form_class=LegalGuardianForm,
            session_key='lg2',
            title='Père / Responsable Légal 2',
            step=3
        ),
        name='regchild_step3'
    ),
    re_path(
        '^regchild_step4\/?(?P<child_id>\d+)?\/?',
        views.RegChildFinal.as_view(),
        name='regchild_step4'),
    path('regperson', views.RegPerson.as_view(), name='regperson'),
    path('modfamily', views.RegFamily.as_view(
        modify=True
    ), name='modfamily'),
    path('delete_this', views.DeleteThis.as_view(), name='delete_this'),
]
