# Generated by Django 5.0.7 on 2024-08-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_all', '0003_add_movies_movies_local_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_departments',
            name='description',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='add_departments',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
