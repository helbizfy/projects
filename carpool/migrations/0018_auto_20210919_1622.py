# Generated by Django 3.1.7 on 2021-09-19 13:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0017_auto_20210919_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='passangers',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ride',
            name='usersRated',
            field=models.ManyToManyField(blank=True, null=True, related_name='usersRated', to=settings.AUTH_USER_MODEL),
        ),
    ]