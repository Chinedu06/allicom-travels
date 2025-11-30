# payments/management/commands/test_payment_signal.py
from django.core.management.base import BaseCommand
from bookings.models import Booking, Notification
from payments.models import Transaction

class Command(BaseCommand):
    help = "Test payment signals by simulating a successful transaction."

    def handle(self, *args, **options):
        booking = Booking.objects.first()
        if not booking:
            self.stdout.write(self.style.ERROR("No booking found. Create one first."))
            return

        txn = Transaction.objects.create(
            booking=booking,
            reference="TXN_CMD_001",
            amount=booking.total_price,
            provider="flutterwave",
            status="pending",
        )
        self.stdout.write(self.style.SUCCESS(f"Created transaction: {txn.reference}"))

        txn.status = "success"
        txn.save()

        booking.refresh_from_db()
        self.stdout.write(self.style.SUCCESS(f"Booking#{booking.pk} -> {booking.status}, {booking.payment_status}"))

        notifications = Notification.objects.filter(message__icontains=str(booking.pk))
        self.stdout.write(self.style.SUCCESS(f"Notifications for Booking#{booking.pk}:"))
        for note in notifications:
            self.stdout.write(f"- {note}")
