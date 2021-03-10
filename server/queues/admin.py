from django.contrib import admin

from . import models

class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','department' , 'max_limit')
    list_display_links = ('name',)
    search_fields = ('name', 'department')
    list_per_page = 20

admin.site.register(models.Queue , QueueAdmin)
admin.site.register(models.VirtualQueue)


