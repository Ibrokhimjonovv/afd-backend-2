# Generated by Django 4.2.17 on 2024-12-30 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_all', '0006_add_movies_genre_add_movies_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_movies',
            name='all_series',
            field=models.CharField(default='', max_length=512),
        ),
    ]
