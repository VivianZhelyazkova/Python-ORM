# Generated by Django 5.0.4 on 2024-08-03 11:37

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mission',
            old_name='astronaut',
            new_name='astronauts',
        ),
        migrations.AlterField(
            model_name='astronaut',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]+$')]),
        ),
        migrations.AlterField(
            model_name='mission',
            name='commander',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commander_missions', to='main_app.astronaut'),
        ),
    ]
