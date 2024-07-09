# Generated by Django 5.0.4 on 2024-07-09 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_owner_alter_drivinglicense_driver_car_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='car',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration', to='main_app.car'),
        ),
    ]
