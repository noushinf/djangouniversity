# Generated by Django 4.1.1 on 2022-11-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='picture',
            field=models.BinaryField(editable=True, null=True),
        ),
    ]
