from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length = 15)
    passport = models.ImageField(default='passport.jpg', upload_to='passport')
    forget_password_code = models.CharField(max_length=6, blank=True, null=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)

class Newsletter(models.Model):
    email = models.CharField(max_length=50)
    status = models.BooleanField(default=True)