from django.contrib import admin

from bookings.models import Booking
from .models import Transaction,Payment

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','booking','provider','amount','status','created_at')
    list_filter = ('provider','status','created_at')
    actions = ['mark_success']

    def mark_success(self, request, queryset):
        for txn in queryset:
            txn.status = Transaction.STATUS_SUCCESS
            txn.save()
            # also mark booking confirmed (and create notifications via booking signals)
            booking = txn.booking
            booking.status = Booking.STATUS_CONFIRMED
            booking.save()
    mark_success.short_description = "Mark selected transactions as success (confirm bookings)"


# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('id','reference','booking','provider','amount','status','created_at')
#     list_filter = ('provider','status','created_at')
#     actions = ['mark_success']

#     def mark_success(self, request, queryset):
#         for txn in queryset:
#             txn.mark_successful()
#     mark_success.short_description = "Mark selected transactions as success (confirm bookings)"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking','reference','amount','status','paid_at')
