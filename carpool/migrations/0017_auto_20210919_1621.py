# Generated by Django 3.1.7 on 2021-09-19 13:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0016_ride_usersrated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='passangers',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ride',
            name='usersRated',
            field=models.ManyToManyField(null=True, related_name='usersRated', to=settings.AUTH_USER_MODEL),
        ),
    ]