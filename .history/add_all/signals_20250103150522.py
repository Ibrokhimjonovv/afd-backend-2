import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Add_departments, Add_movies, MovieSeries

REMOTE_SERVER_URL = "http://127.0.0.1:8000/afd/second-backend/"

# Departamentlar uchun signal
@receiver(post_save, sender=Add_departments)
def sync_department(sender, instance, created, **kwargs):
    if created:
        data = {
            "department_name": instance.department_name,
            "image": instance.image.url if instance.image else None,
            "description": instance.description,
        }
        try:
            requests.post(f"{REMOTE_SERVER_URL}add-department/", json=data)
        except requests.exceptions.RequestException as e:
            print(f"Error syncing department: {e}")

# Filmlar uchun signal
@receiver(post_save, sender=Add_movies)
def sync_movies(sender, instance, created, **kwargs):
    if created:
        data = {
            "movies_name": instance.movies_name,
            "movies_description": instance.movies_description,
            "movies_url": instance.movies_url,
            "movies_local": instance.movies_local.url if instance.movies_local else None,
            "country": instance.country,
            "year": instance.year,
            "genre": instance.genre,
        }
        try:
            requests.post(f"{REMOTE_SERVER_URL}add-movie/", json=data)
        except requests.exceptions.RequestException as e:
            print(f"Error syncing movie: {e}")

# Seriyalar uchun signal
@receiver(post_save, sender=MovieSeries)
def sync_movie_series(sender, instance, created, **kwargs):
    if created:
        data = {
            "movie_id": instance.movie.id,
            "title": instance.title,
            "video_url": instance.video_url,
            "video_file": instance.video_file.url if instance.video_file else None,
        }
        try:
            requests.post(f"{REMOTE_SERVER_URL}add-series/", json=data)
        except requests.exceptions.RequestException as e:
            print(f"Error syncing movie series: {e}")
