from django.contrib import admin

from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'description')
    list_filter = ('date', 'time')
    search_fields = ('user__username', 'description')

