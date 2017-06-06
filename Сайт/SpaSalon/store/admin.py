from django.contrib import admin
from django.contrib.admin import ModelAdmin

import store

from .models import News, Employee, Service, Visit


class VisitAdmin(ModelAdmin):
    list_display = ('client_name', 'visit_date', 'service', 'employee', 'notes')
    ordering = ['client_name', 'visit_date', 'service', 'employee', 'notes']
    search_fields = ['client_name', 'visit_date', 'service__name', 'employee__full_name', 'notes']

admin.site.register(Visit, VisitAdmin)

admin.site.register(News)
admin.site.register(Employee)
admin.site.register(Service)
#admin.site.register(Visit)
