# Generated by Django 3.1.7 on 2021-07-14 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0009_auto_20210714_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='ride',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ride', to='carpool.ride'),
        ),
    ]
