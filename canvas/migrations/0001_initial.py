# Generated by Django 4.1.7 on 2023-04-16 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(auto_created=True, help_text='LTI Course ID', max_length=512, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='LTI Course name', max_length=120)),
                ('register_date', models.DateTimeField(auto_now=True, help_text='Timestamp when the course first appeared in our system')),
                ('deployment_id', models.CharField(help_text='Relation to corresponding deployment on an LTI Platform', max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='LTIUser',
            fields=[
                ('lti_user_id', models.UUIDField(help_text='User sub as referred by the LTI platform', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='User name in LTI platform', max_length=50)),
                ('email', models.EmailField(help_text='User email in the LTI platform', max_length=254, unique=True)),
            ],
        ),
    ]
