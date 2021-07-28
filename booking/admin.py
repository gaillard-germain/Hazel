from django.contrib import admin
from django.http import HttpResponse
import csv
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
class BookingAdmin(admin.ModelAdmin):
    list_display = ('child', 'categorie', 'slot', 'whole', 'validated')
    list_editable = ('whole', 'validated')
    list_filter = ('validated', CategoryListFilter,)
    date_hierarchy = 'slot__day'
    ordering = ('slot__day',)
    actions = ["export_as_csv"]

    def categorie(self, obj):
        """ Custom admin field to display children's categories """

        return obj.child.category

    def export_as_csv(self, request, queryset):
        """ Adds the action to export a queryset as a csv file """

        meta = self.model._meta
        fields = [field for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename={}.csv'.format(meta)
        )
        writer = csv.writer(response)

        writer.writerow(['nom', 'prénom', 'date', 'journée', 'demi-journée'])

        queryset = queryset.exclude(validated=False)

        for obj in queryset:
            data_row = []
            for field in fields:
                if field.name == 'child':
                    value = getattr(obj, field.name).lastname
                    data_row.append(value)
                    value = getattr(obj, field.name).firstname
                    data_row.append(value)

                elif field.name == 'slot':
                    value = getattr(obj, field.name).day
                    data_row.append(value)

                elif field.name == 'whole':
                    value = getattr(obj, field.name)
                    if value:
                        data_row.append('X')
                        data_row.append('')
                        
                    else:
                        data_row.append('')
                        data_row.append('X')

            writer.writerow(data_row)

        return response

    description = "Exporter les Réservations sélectionnées au format CSV"
    export_as_csv.short_description = description
