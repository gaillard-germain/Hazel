from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Family, Child, Adult


admin.site.register(User, UserAdmin)
admin.site.register(Family)
admin.site.register(Child)
admin.site.register(Adult)
