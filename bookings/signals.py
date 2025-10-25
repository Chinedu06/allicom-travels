from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from .models import Booking, Notification
from services.models import Service
from payments.models import Transaction, Payment

def send_notification(recipient, message):
    # lightweight helper (in-app)
    if recipient is None:
        return
    Notification.objects.create(recipient=recipient, message=message)

@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance: Booking, created, **kwargs):
    """
    - When a new booking is created -> notify admins (recipient=None for admin/global) and operator.
      Admin notification: we'll set recipient to None to indicate 'global' (admins should poll admin UI).
      Additionally, notify operator that a booking was created (so they can see in their dashboard).
    - When booking status changes to confirmed/rejected -> notify tourist and operator (operator only after confirm).
    """
    # created -> notify admins and operator
    if created:
        # Notify admins: create a Notification with recipient=None (you may change to send to all admin users)
        Notification.objects.create(
            recipient=None,
            message=f"New booking #{instance.pk} for '{instance.service.title}' by {instance.given_name} {instance.surname}"
        )

        # Notify operator that their service has been booked (informational)
        operator = instance.service.operator
        if operator:
            Notification.objects.create(
                recipient=operator,
                message=f"Your service '{instance.service.title}' has a new booking #{instance.pk}."
            )
        return

    # not created: check status transitions
    # A simple approach: lookup the previous status by querying DB (safe because this runs after save)
    try:
        old = Booking.objects.get(pk=instance.pk)
    except Booking.DoesNotExist:
        old = None

    # If status changed (we compare instance.status to `old.status`), notify accordingly.
    # Note: since this is post_save, old & instance will be same; so we store previous value in pre_save handler
    # Alternative: store previous status in instance._previous_status in pre_save (we implement below).
    prev_status = getattr(instance, "_previous_status", None)
    new_status = instance.status

    if prev_status != new_status:
        # Tourist notifications on approve/reject
        if new_status == Booking.STATUS_CONFIRMED:
            if instance.user:
                Notification.objects.create(
                    recipient=instance.user,
                    message=f"Your booking #{instance.pk} for '{instance.service.title}' has been approved."
                )
            else:
                # if anonymous, use email fallback in your worker/email system (not implemented here)
                pass

            # Notify operator AFTER admin confirm
            operator = instance.service.operator
            if operator:
                Notification.objects.create(
                    recipient=operator,
                    message=f"Booking #{instance.pk} for '{instance.service.title}' has been approved by admin."
                )

        elif new_status == Booking.STATUS_REJECTED:
            if instance.user:
                Notification.objects.create(
                    recipient=instance.user,
                    message=f"Your booking #{instance.pk} for '{instance.service.title}' has been rejected. Reason: {instance.admin_note or 'No reason provided.'}"
                )

@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance: Booking, **kwargs):
    # store previous status for post_save comparison
    if instance.pk:
        try:
            old = Booking.objects.get(pk=instance.pk)
            instance._previous_status = old.status
        except Booking.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


# Optional: when a Transaction becomes successful, sync created Payment -> booking & notify user/operator/admin
@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance: Transaction, created, **kwargs):
    # only act on status success
    if instance.status == Transaction.STATUS_SUCCESS:
        # ensure booking/payment synced using model method
        try:
            instance.mark_successful()
        except Exception:
            # avoid raising from signal; log will pick this up
            import logging
            logging.exception("Error in transaction_post_save.mark_successful")

        # notify user that payment succeeded (if user attached to booking)
        booking = instance.booking
        if booking.user:
            Notification.objects.create(
                recipient=booking.user,
                message=f"Payment received for booking #{booking.pk}. Your booking will be processed."
            )
        # notify admin too
        Notification.objects.create(
            recipient=None,
            message=f"Transaction {instance.reference} succeeded for booking #{booking.pk}."
        )
