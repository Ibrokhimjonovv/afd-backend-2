from django.db import models

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
    

    def __str__(self):
        return self.movies_name
    
class MovieSeries(models.Model):
    movie = models.ForeignKey(Add_movies, on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=128)
    video_url = models.CharField(max_length=1024)  # Seriyalar uchun URLField
    video_file = models.FileField(null=True, blank=True)  # Agar fayl orqali yuklash kerak bo'lsa

    def __str__(self):
        return f"{self.movie.movies_name} - {self.title}"
    