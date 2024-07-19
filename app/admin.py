from django.contrib import admin
from app.models import *


class VisitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/visit/visit_change_list.html'
    list_display = ['type', 'bot_user', 'address', 'comment', 'datetime', 'location']
    search_fields = ['address']
    list_filter = ('bot_user', 'type',)

admin.site.register(Visit, VisitAdmin)