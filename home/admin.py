from django.contrib import admin
from .models import Price, Category, Activity, Agenda


class ActivityInLine(admin.TabularInline):
    model = Activity
    extra = 1


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    inlines = [ActivityInLine, ]
    fields = ('entry',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('family_quotient', 'day', 'half_day')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
