from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    used= models.BooleanField(default=False)

    def is_valid(self):
        expiry = self.created_at + timedelta(hours=1)
        return not self.used and timezone.now() < expiry
    
    def __str__(self):
        return f"Reset token for {self.user.email}"
    

    