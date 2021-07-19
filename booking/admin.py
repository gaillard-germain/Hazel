from django.contrib import admin
from .models import Period, Booking, Slot

admin.site.register(Period)
admin.site.register(Booking)


class BookingInLine(admin.TabularInline):
    model = Booking
    extra = 0


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    readonly_fields = ('day', 'is_full',)
    inlines = [BookingInLine, ]
