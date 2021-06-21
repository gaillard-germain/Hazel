from django.contrib import admin
from .models import Price, Category, Activity, Agenda


admin.site.register(Price)
admin.site.register(Category)



class ActivityInLine(admin.TabularInline):
    model = Activity
    extra = 1


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    inlines = [ActivityInLine, ]
    fields = ('entry',)
