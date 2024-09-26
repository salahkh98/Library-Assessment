from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # You can add additional fields here if needed
    email = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # Override groups and user_permissions to specify related names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change related name
        blank=True,
    )
    def __str__(self):
        return self.username