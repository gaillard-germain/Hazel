from django.contrib import admin
from .models import Family, Child, Adult


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    search_fields = ('lastname', 'firstname',)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    search_fields = ('use_name',)


@admin.register(Adult)
class AdultAdmin(admin.ModelAdmin):
    search_fields = ('lastname', 'firstname',)
