# Generated by Django 3.1.7 on 2021-06-08 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_fallower_fallowing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 8, 22, 13, 42, 872528)),
        ),
    ]