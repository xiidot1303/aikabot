from django.contrib import admin
from app.models import *

class VisitAdmin(admin.ModelAdmin):
    list_display = ['type', 'bot_user', 'address', 'datetime', 'location']

admin.site.register(Visit, VisitAdmin)