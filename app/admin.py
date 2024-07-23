from django.contrib import admin
from app.models import *


class VisitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/visit/visit_change_list.html'
    list_display = ['type', 'bot_user', 'address', 'comment', 'datetime', 'location']
    search_fields = ['address']
    list_filter = ('bot_user', 'type',)

class DoctorAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

admin.site.register(Visit, VisitAdmin)
admin.site.register(Doctor, DoctorAdmin)