# Generated by Django 3.0.6 on 2021-03-17 15:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TinTuc', '0003_auto_20210309_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='new_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
