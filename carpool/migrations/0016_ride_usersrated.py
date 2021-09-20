# Generated by Django 3.1.7 on 2021-09-19 13:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0015_ride_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='usersRated',
            field=models.ManyToManyField(related_name='usersRated', to=settings.AUTH_USER_MODEL),
        ),
    ]