from django.contrib import admin, messages
from .models import Period, Booking, Slot
from registration.models import Child
from home.models import Category


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


class CategoryListFilter(admin.SimpleListFilter):
    title = ('Groupe')
    parameter_name = 'groupe'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        tuples_list = []
        for category in categories:
            tuples_list.append((category.name, (category.name)))

        return tuples_list

    def queryset(self, request, queryset):
        if self.value():
            category = Category.objects.get(name=self.value())
            children = Child.objects.exclude(category=category)
            for child in children:
                queryset = queryset.exclude(child=child)

            return queryset


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('child', 'categorie', 'slot', 'whole', 'validated')
    list_editable = ('whole', 'validated')
    list_filter = ('slot',CategoryListFilter)
    ordering = ('slot',)

    def categorie(self, obj):
        child = Child.objects.get(booking=obj)
        return child.category

    def save_model(self, request, obj, form, change):
        try:
            obj = Booking.objects.get(
                child=form.cleaned_data.get('child'),
                slot=form.cleaned_data.get('slot')
            )
            self.message_user(request, 'Cette réservation existe déjà',
                              level=messages.WARNING)

        except Booking.DoesNotExist:
            super().save_model(request, obj, form, change)
