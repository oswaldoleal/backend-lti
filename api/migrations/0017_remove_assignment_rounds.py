# Generated by Django 4.2a1 on 2023-03-31 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_gamedata_user_input_run_user_input'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='rounds',
        ),
    ]
