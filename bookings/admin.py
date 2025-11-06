from django.contrib import admin
from .models import Booking, Notification

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'service__title')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient_display', 'short_message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    actions = ['mark_as_read', 'mark_as_unread']
    list_per_page = 20

    def short_message(self, obj):
        """Display a truncated preview of the message for quick scanning."""
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message
    short_message.short_description = "Message"

    def recipient_display(self, obj):
        """Show 'Admin/All' for None recipients."""
        return obj.recipient.username if obj.recipient else "Admin / All"
    recipient_display.short_description = "Recipient"

    @admin.action(description="Mark selected notifications as read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")

    @admin.action(description="Mark selected notifications as unread")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notification(s) marked as unread.")
