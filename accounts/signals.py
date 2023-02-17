# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from notifications.models import Notification
# from .models import Notification, User

# @receiver(post_save, sender=User)
# def post_save_create_profile(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(user=instance)