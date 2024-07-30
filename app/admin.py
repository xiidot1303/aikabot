from django.contrib import admin
from app.models import *
from rangefilter.filters import DateRangeFilter

class VisitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/visit/visit_change_list.html'
    list_display = ['type', 'bot_user', 'address', 'comment', 'datetime', 'location']
    search_fields = ['address']
    list_filter = ('bot_user', 'type', ('datetime', DateRangeFilter))

class DoctorAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class PharmacyAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class PartnerAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


admin.site.register(Visit, VisitAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(Partner, PartnerAdmin)