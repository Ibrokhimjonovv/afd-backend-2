from django.db import models
from users.models import User

# Create your models here.

class Add_departments(models.Model):
    department_name = models.CharField(max_length=512)
    image = models.FileField(null=True, blank=True)
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.department_name

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