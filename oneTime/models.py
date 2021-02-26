from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from oneTime.utils import generate_jti

User = settings.AUTH_USER_MODEL


# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    logged_in_before = models.BooleanField(default=False)
    stream_link = models.CharField(max_length=1000, null=True, blank=True)
    ip = models.CharField(max_length=100, null=True, blank=True)
    jti = models.CharField(
        "jwt id",
        max_length=64,
        blank=False,
        null=False,
        editable=False,
        default=generate_jti,
        help_text="JWT tokens for the user get revoked when JWT id has regenerated.",
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        LoggedInUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.logged_in_user.save()
