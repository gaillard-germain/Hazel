from django.contrib import admin
from .models import Period, Booking, Slot
from registration.models import Child
from home.models import Category
from registration.admin import ChildInline


class BookingInLine(admin.TabularInline):
    model = Booking
    extra = 0


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    search_fields = ('day',)
    readonly_fields = ('day', 'is_full',)
    inlines = [BookingInLine,]
    list_filter = ('day',)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('child', 'slot', 'whole', 'validated')
