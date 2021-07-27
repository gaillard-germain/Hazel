from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Period, Booking, Slot
from registration.models import Child
from home.models import Category


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        fields = [field for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename={}.csv'.format(meta)
        )
        writer = csv.writer(response)

        writer.writerow([field.verbose_name for field in fields])
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                data_row.append(value)
            writer.writerow(data_row)
            # row = writer.writerow(
            #     [getattr(obj, field) for field in field_names]
            # )

        return response

    description = "Exporter les Réservations sélectionnées au format CSV"
    export_as_csv.short_description = description


class BookingInLine(admin.TabularInline):
    model = Booking
    extra = 0


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    search_fields = ('day',)
    readonly_fields = ('day', 'is_full',)
    inlines = [BookingInLine, ]
    list_filter = ('day',)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')


class CategoryListFilter(admin.SimpleListFilter):
    """ Custom filter to choose children's category """

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
class BookingAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('child', 'categorie', 'slot', 'whole', 'validated')
    list_editable = ('whole', 'validated')
    list_filter = ('validated', CategoryListFilter, 'slot',)
    ordering = ('slot',)
    actions = ["export_as_csv"]

    def categorie(self, obj):
        """ Custom admin field to display children's categories """

        child = Child.objects.get(booking=obj)
        return child.category
