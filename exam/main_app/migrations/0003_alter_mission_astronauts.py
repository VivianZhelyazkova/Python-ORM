# Generated by Django 5.0.4 on 2024-08-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_rename_astronaut_mission_astronauts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='astronauts',
            field=models.ManyToManyField(related_name='missions', to='main_app.astronaut'),
        ),
    ]
