from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Blog, User


# def send_notification_to_new_user(sender, instance, **kwargs):
#     """
#     Sends a notification to the user when their account is created.
#     """
#     # Get the user who created the account.
#     user = instance.created_by

#     # Create a notification object.
#     # notification = Notification(
#     #     user=user,
#     #     message="Your account has been created.",
#     # )
#     print("its workking ")
#     # Send the notification to the user.
#     # notification.send()


# @receiver(post_save, sender=Blog)
# def my_signal_handler(sender, instance, **kwargs):
#     send_notification_to_new_user(sender, instance, **kwargs)
