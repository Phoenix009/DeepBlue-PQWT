from django.contrib import admin

from . import models

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','hospital','order')
    list_display_links = ('name',)
    search_fields = ('name', 'hospital')
    list_per_page = 20

admin.site.register(models.Department , DepartmentAdmin)
