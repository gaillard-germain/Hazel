from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Family


admin.site.register(User, UserAdmin)
admin.site.register(Family)
