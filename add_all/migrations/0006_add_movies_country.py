# Generated by Django 5.0.7 on 2024-08-23 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_all', '0005_swiperfilms'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_movies',
            name='country',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]
