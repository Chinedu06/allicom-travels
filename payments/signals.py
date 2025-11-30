# import logging
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Transaction
# from bookings.models import Notification, Booking

# logger = logging.getLogger('payments')  # 🟢 Use structured logger


# @receiver(post_save, sender=Transaction)
# def handle_transaction_status_change(sender, instance, created, **kwargs):
#     """
#     Triggered when a Transaction is created or updated.
#     Updates related Booking & creates Notification records.
#     """
#     try:
#         if created:
#             logger.info(f"New transaction created: {instance.reference}")
#             return

#         # 🟢 Handle success — mark booking as confirmed and notify user/admin
#         if instance.status == 'success':
#             booking = instance.booking
#             booking.payment_status = 'paid'
#             booking.status = Booking.STATUS_CONFIRMED
#             booking.save()

#             # Notify Admin
#             Notification.objects.create(
#                 recipient=None,
#                 message=f"Payment confirmed for Booking#{booking.pk} ({instance.reference})."
#             )

#             # Notify User
#             if booking.user:
#                 Notification.objects.create(
#                     recipient=booking.user,
#                     message=f"Your payment for Booking#{booking.pk} was successful. Thank you!"
#                 )

#             logger.info(f"Booking#{booking.pk} marked as paid and confirmed.")

#         elif instance.status == 'failed':
#             Notification.objects.create(
#                 recipient=None,
#                 message=f"Payment FAILED for Booking#{instance.booking.pk} (Ref: {instance.reference})."
#             )
#             logger.warning(f"Payment failed for Booking#{instance.booking.pk}")

#     except Exception as e:
#         logger.error(f"Error processing transaction signal: {e}")

import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction           # ✅ only Transaction comes from payments.models
from bookings.models import Booking, Notification   # ✅ Booking + Notification come from bookings app


logger = logging.getLogger('bookings')

@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance, **kwargs):
    """
    Capture old status before saving to detect changes.
    """
    if instance.pk:
        try:
            old = Booking.objects.get(pk=instance.pk)
            instance._old_status = old.status
        except Booking.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance, created, **kwargs):
    """
    Trigger notifications on creation and status updates.
    Booking-centric notifications remain here (operator/user/admin).
    """
    try:
        def create_notification(recipient, message):
            Notification.objects.create(recipient=recipient, message=message)

        service = getattr(instance, "service", None)
        operator = getattr(service, "operator", None) if service else None

        # --- New booking ---
        if created:
            if operator:
                create_notification(
                    operator,
                    f"New booking #{instance.pk} created for your service \"{service.title}\"."
                )
            # also notify admin/global
            create_notification(None, f"New booking #{instance.pk} created for service \"{service.title}\".")
            return

        old_status = getattr(instance, "_old_status", None)
        new_status = instance.status
        if old_status == new_status:
            return  # No change

        # --- Booking confirmed ---
        if new_status == Booking.STATUS_CONFIRMED:
            if operator:
                create_notification(operator, f"Booking #{instance.pk} for \"{service.title}\" has been approved.")
            if instance.user:
                create_notification(instance.user, f"Your booking #{instance.pk} has been approved.")

        # --- Booking rejected ---
        elif new_status == Booking.STATUS_REJECTED:
            reason = instance.admin_note or "No reason provided."
            if operator:
                create_notification(operator, f"Booking #{instance.pk} was rejected. Reason: {reason}")
            if instance.user:
                create_notification(instance.user, f"Your booking #{instance.pk} was rejected. Reason: {reason}")

        # --- Booking cancelled ---
        elif new_status == Booking.STATUS_CANCELLED:
            create_notification(None, f"Booking #{instance.pk} has been cancelled by {getattr(instance.user, 'username', 'Unknown')}.")
            if operator:
                create_notification(operator, f"Booking #{instance.pk} has been cancelled.")
            if instance.user:
                create_notification(instance.user, f"Your booking #{instance.pk} has been cancelled.")

    except Exception:
        logger.exception("Error in booking signals")

# -------------------------
# CHANGED: Duplicate Transaction handler removed (commented)
# -------------------------
# We previously had a post_save receiver for Transaction here. That handler was moved to
# payments/signals.py to centralize payment -> booking logic and avoid duplicate notifications.
#
# Keeping this commented block for reference (do not re-enable unless you remove the payments handler).
#
# from payments.models import Transaction
# @receiver(post_save, sender=Transaction)
# def booking_transaction_handler(sender, instance, created, **kwargs):
#     pass  # moved to payments.signals
