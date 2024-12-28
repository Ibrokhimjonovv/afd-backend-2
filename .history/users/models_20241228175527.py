
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=512)
    password = models.CharField(max_length=32)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
