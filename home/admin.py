from django.contrib import admin
from .models import Price, Category, Activity, Agenda


class ActivityInLine(admin.TabularInline):
    model = Activity
    extra = 1


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'day')
    ordering = ('-day',)
    date_hierarchy = 'day__entry'


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    inlines = [ActivityInLine, ]
    fields = ('entry',)
    date_hierarchy = 'entry'


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('family_quotient', 'day', 'half_day')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
