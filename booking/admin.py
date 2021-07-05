from django.contrib import admin
from .models import Period, Booking, Slot

admin.site.register(Period)
admin.site.register(Booking)


class BookingInLine(admin.TabularInline):
    model = Booking
    extra = 1


@admin.register(Slot)
class lotAdmin(admin.ModelAdmin):
    inlines = [BookingInLine, ]
