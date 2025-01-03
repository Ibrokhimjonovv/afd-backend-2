from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from django.conf import settings

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
        url = settings.DEPARTMENT_API_URL  # Global URL'dan foydalanamiz
        data = {
            'department_name': instance.department_name,
            'description': instance.description,
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
    movies_description = models.CharField(max_length=512)
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

@receiver(post_save, sender=Add_movies)
def send_movie_to_other_api(sender, instance, created, **kwargs):
    if created:  # faqat yangi film qo'shilganda ishlaydi
        url = settings.MOVIE_API_URL  # Global URL'dan foydalanamiz
        data = {
            'movies_name': instance.movies_name,
            'movies_description': instance.movies_description,
            'country': instance.country,
            'year': instance.year,
            'genre': instance.genre,
            'all_series': instance.all_series,
            'count': instance.count,
            'movies_url': instance.movies_url,
            'movies_preview_url': instance.movies_preview_url,
            'department': instance.add_departments.id,  # Departmentni to'g'ri yuboring
        }

        files = {}

        if instance.movies_local:
            files['movie_local'] = instance.movies_local

        if instance.movies_preview:
            files['movies_preview'] = instance.movies_preview

        response = requests.post(url, data=data, files=files)


        if response.status_code == 201:
            print("Movie successfully sent to the other project")
        else:
            print("Failed to send movie to the other project")

class MovieSeries(models.Model):
    movie = models.ForeignKey(Add_movies, on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=128)
    video_url = models.CharField(max_length=1024)  # Seriyalar uchun URLField
    video_file = models.FileField(null=True, blank=True)  # Agar fayl orqali yuklash kerak bo'lsa

    def __str__(self):
        return f"{self.movie.movies_name} - {self.title}"

@receiver(post_save, sender=MovieSeries)
def send_movie_series_to_other_api(sender, instance, created, **kwargs):
    if created:  # faqat yangi serial qo'shilganda ishlaydi
        url = settings.MOVIE_SERIES_API_URL  # Global URL'dan foydalanamiz
        data = {
            'movie_name': instance.movie.movies_name,
            'title': instance.title,
            'video_url': instance.video_url,
        }

        # Agar video faylini yuborish kerak bo'lsa:
        if instance.video_file:
            files = {'video_file': instance.video_file}
            response = requests.post(url, data=data, files=files)
        else:
            response = requests.post(url, data=data)

        if response.status_code == 201:
            print("Movie Series successfully sent to the other project")
        else:
            print("Failed to send movie series to the other project")

# Saqlangan film modeli
class SavedFilm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foydalanuvchi
    film = models.ForeignKey(Add_movies, on_delete=models.CASCADE)  # Saqlangan film
    saved_at = models.DateTimeField(auto_now_add=True)  # Qachon saqlanganini ko'rsatish

    def __str__(self):
        return f'{self.user.username} saved {self.film.movies_name}'

@receiver(post_save, sender=SavedFilm)
def send_saved_film_to_other_api(sender, instance, created, **kwargs):
    if created:  # faqat yangi saqlangan film qo'shilganda ishlaydi
        url = settings.SAVED_FILM_API_URL  # Global URL'dan foydalanamiz
        data = {
            'user': instance.user.username,
            'film': instance.film.movies_name,
            'saved_at': instance.saved_at,
        }

        response = requests.post(url, data=data)

        if response.status_code == 201:
            print("Saved Film successfully sent to the other project")
        else:
            print("Failed to send saved film to the other project")
