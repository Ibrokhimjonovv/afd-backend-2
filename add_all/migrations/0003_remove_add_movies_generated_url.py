# Generated by Django 4.2.17 on 2025-01-03 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('add_all', '0002_add_movies_generated_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='add_movies',
            name='generated_url',
        ),
    ]
