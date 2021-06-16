from django.urls import path, include

from . import views
from .forms import LegalGuardianForm


app_name = 'registration'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout', views.logout_request, name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('myaccount', views.ManageAccount.as_view(), name='myaccount'),
    path('regchild_step1', views.RegChild.as_view(), name='regchild_step1'),
    path(
        'regchild_step2',
        views.RegChild.as_view(
            form_class=LegalGuardianForm,
            session_key = 'lg1',
            title = 'Mère / Responsable Légal 1',
            step = 2
        ),
        name='regchild_step2'
    ),
    path(
        'regchild_step3',
        views.RegChild.as_view(
            form_class=LegalGuardianForm,
            session_key = 'lg2',
            title = 'Père / Responsable Légal 2',
            step = 3
        ),
        name='regchild_step3'
    ),
    path('regchild_step4', views.RegChildFinal.as_view(),
        name='regchild_step4'),
    path('regperson', views.RegPerson.as_view(), name='regperson'),
]
