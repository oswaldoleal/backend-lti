# Generated by Django 4.2a1 on 2023-03-29 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_assignment_attempts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedata',
            name='user_input',
        ),
        migrations.AddField(
            model_name='run',
            name='user_input',
            field=models.JSONField(default=dict),
        ),
    ]
