from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'package', 'given_name', 'contact_number', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('given_name', 'surname', 'contact_number', 'email', 'service__title')
    readonly_fields = ('created_at', 'updated_at')
