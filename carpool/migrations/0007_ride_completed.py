# Generated by Django 3.1.7 on 2021-07-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0006_auto_20210704_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]