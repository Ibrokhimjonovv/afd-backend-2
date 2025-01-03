import requests
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
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
        return self.username

# Signal to send user data to another API when a new user is created
@receiver(post_save, sender=User)
def send_user_to_other_api(sender, instance, created, **kwargs):
    if created:  # faqat yangi foydalanuvchi qo'shilganda ishlaydi
        url = 'http://localhost:1112/afd-platform/backend/urls/users/'  # Boshqa loyihangizning API endpointi

        # Foydalanuvchi ma'lumotlarini tayyorlash
        data = {
            'first_name': instance.firstName,
            'last_name': instance.last_name,
            'username': instance.username,
            'email': instance.email,
            'dateJoined': instance.date_joined,
            'password': instance.password,
        }

        # Agar profile_image bo'lsa, uni yuborish
        if instance.profile_image:
            files = {'profile_image': instance.profile_image}
            response = requests.post(url, data=data, files=files)
        else:
            response = requests.post(url, data=data)

        if response.status_code == 201:
            print(f"User {instance.username} successfully sent to the other project.")
        else:
            print(f"Failed to send user {instance.username} to the other project. Status code: {response.status_code}, Status text: {response.text}")