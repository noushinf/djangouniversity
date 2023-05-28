# Generated by Django 4.2.1 on 2023-05-23 07:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0005_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='comments',
            field=models.ManyToManyField(related_name='book_comments', through='library.Comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
