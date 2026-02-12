from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_premium = models.BooleanField(default=False)
    tier = models.CharField(
        max_length=10,
        choices=[("Free", "Free"), ("Premium", "Premium"), ("Admin", "Admin")],
        default="Free",
    )
