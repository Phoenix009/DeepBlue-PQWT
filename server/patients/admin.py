from django.contrib import admin

from . import models

class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name','otp' , 'verified', 'email')
    list_display_links = ('full_name',)
    search_fields = ('first_name', 'last_name' , 'email')
    list_per_page = 20

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

admin.site.register(models.Patient , PatientAdmin)

