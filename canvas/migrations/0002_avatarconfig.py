# Generated by Django 4.2 on 2023-04-30 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvatarConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.JSONField()),
                ('user', models.ForeignKey(help_text='Relation to lti user', on_delete=django.db.models.deletion.CASCADE, related_name='ltiUser', to='canvas.ltiuser')),
            ],
        ),
    ]
