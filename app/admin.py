from django.contrib import admin
from django.utils.html import format_html
from app.models import *
from rangefilter.filters import DateRangeFilter
from django.contrib.admin import SimpleListFilter
from bot.models import Fillial

class FillialFilter(SimpleListFilter):
    title = 'Филиал'
    parameter_name = 'fillial'

    def lookups(self, request, model_admin):
        return [(fillial.id, fillial.title) for fillial in Fillial.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bot_user__fillial_id=self.value())
        return queryset

class VisitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/visit/visit_change_list.html'
    list_display = ['type', 'bot_user', 'address', 'comment', 'datetime', 'location_link']
    search_fields = ['address']
    list_filter = ('bot_user', 'type', FillialFilter, ('datetime', DateRangeFilter))

    def changelist_view(self, request, extra_context=None):
        # Add the URL parameters to the context
        if extra_context is None:
            extra_context = {}
        extra_context['datetime__range__gte'] = request.GET.get('datetime__range__gte', "")
        extra_context['datetime__range__lte'] = request.GET.get('datetime__range__lte', "")
        extra_context['fillial'] = request.GET.get('fillial', "")

        return super().changelist_view(request, extra_context=extra_context)

    def location_link(self, obj):
        link = f"https://www.google.com/maps?q={obj.lat},{obj.lon}"
        return format_html(
            '<a href="{}">{}</a>', 
            link, 
            obj.location if obj.location else link
            )


class DoctorAdmin(admin.ModelAdmin):
    change_list_template = 'admin/doctor/doctor_change_list.html'
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class PharmacyAdmin(admin.ModelAdmin):
    change_list_template = 'admin/pharmacy/pharmacy_change_list.html'
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class PartnerAdmin(admin.ModelAdmin):
    change_list_template = 'admin/partner/partner_change_list.html'
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


admin.site.register(Visit, VisitAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(Partner, PartnerAdmin)