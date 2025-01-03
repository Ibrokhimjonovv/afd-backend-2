from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

# Create your models here.

class Add_departments(models.Model):
    department_name = models.CharField(max_length=512)
    image = models.FileField(null=True, blank=True)
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.department_name

@receiver(post_save, sender=Add_departments)
def send_department_to_other_api(sender, instance, created, **kwargs):
    if created:  # faqat yangi ma'lumot qo'shilganda ishlaydi
        url = 'http://192.168.1.6:1111/afd-platform/backend/urls/departments/'  # Boshqa loyihangizning API endpointi
        data = {
            'department_name': instance.department_name,
            'description': instance.description,
            # agar image faylini yuborish kerak bo'lsa, uni base64 formatida yuborishingiz mumkin
        }

        # Agar rasm faylini yuborish kerak bo'lsa:
        if instance.image:
            files = {'image': instance.image}
            response = requests.post(url, data=data, files=files)
        else:
            response = requests.post(url, data=data)

        if response.status_code == 201:
            print("Department successfully sent to the other project")
        else:
            print("Failed to send department to the other project")

class Add_movies(models.Model):
    add_departments = models.ForeignKey(Add_departments, on_delete=models.CASCADE, related_name="add_departments")
    movies_preview = models.FileField(null=True, blank=True, upload_to="movies_images")
    movies_preview_url = models.CharField(max_length=5024, blank=True, null=True)
    movies_name = models.CharField(max_length=128)
    movies_description= models.CharField(max_length=512)
    movies_url = models.CharField(max_length=10000000, null=True, blank=True)
    movies_local = models.FileField(null=True, blank=True)
    country = models.CharField(max_length=32)
    count = models.PositiveIntegerField(default=0)
    year = models.CharField(max_length=32, default="")
    genre = models.CharField(max_length=512, default="")
    all_series = models.CharField(max_length=512, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movies_name
    
class MovieSeries(models.Model):
    movie = models.ForeignKey(Add_movies, on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=128)
    video_url = models.CharField(max_length=1024)  # Seriyalar uchun URLField
    video_file = models.FileField(null=True, blank=True)  # Agar fayl orqali yuklash kerak bo'lsa

    def __str__(self):
        return f"{self.movie.movies_name} - {self.title}"
    
# Saqlangan film modeli
class SavedFilm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foydalanuvchi
    film = models.ForeignKey(Add_movies, on_delete=models.CASCADE)  # Saqlangan film
    saved_at = models.DateTimeField(auto_now_add=True)  # Qachon saqlanganini ko'rsatish

    def __str__(self):
        return f'{self.user.username} saved {self.film.name}'