from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Family, Child, Adult, Category


admin.site.register(User, UserAdmin)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    search_fields = ('lastname', 'firstname',)
    list_filter = ('category',)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    search_fields = ('use_name',)


@admin.register(Adult)
class AdultAdmin(admin.ModelAdmin):
    search_fields = ('lastname', 'firstname',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
