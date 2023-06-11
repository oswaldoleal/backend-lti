# Generated by Django 4.2 on 2023-05-23 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0002_avatarconfig'),
        ('api', '0003_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionbank',
            name='user',
            field=models.ForeignKey(default='6315a814-2732-42c3-ac4f-2fc15c0fe26e', help_text='Relation to corresponding user', on_delete=django.db.models.deletion.CASCADE, to='canvas.ltiuser'),
            preserve_default=False,
        ),
    ]