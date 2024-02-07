from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# a new profile is created everytime a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# after creating that profile save it
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()