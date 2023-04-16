# Generated by Django 4.2a1 on 2023-03-28 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_run_state_alter_assignment_register_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='attempts',
            field=models.PositiveSmallIntegerField(default=3, help_text='Number of attempts a student has for the assignment'),
            preserve_default=False,
        ),
    ]
