"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


def trigger_error(request):
    division_by_zero = 1 / 0


admin.site.site_header = 'Administration de HAZEL'
admin.site.site_title = 'HAZEL'
admin.site.index_title = "Bienvenue sur le site d'administration de HAZEL"

urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('registration/', include('registration.urls')),
    path('booking/', include('booking.urls')),
]
