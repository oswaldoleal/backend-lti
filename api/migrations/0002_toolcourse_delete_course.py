# Generated by Django 4.2a1 on 2023-03-21 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0003_course'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateTimeField(auto_created=True, help_text='Timestamp when the course first appeared in our system')),
                ('name', models.CharField(help_text='Course name', max_length=120)),
                ('course', models.ForeignKey(help_text='Relation to corresponding course on an LTI Platform', on_delete=django.db.models.deletion.CASCADE, related_name='course', to='canvas.course')),
            ],
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
