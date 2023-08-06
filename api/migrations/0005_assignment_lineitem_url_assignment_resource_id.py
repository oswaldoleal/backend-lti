# Generated by Django 4.1.7 on 2023-07-23 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_questionbank_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='lineitem_url',
            field=models.URLField(default='', help_text='Direct URL for the item on the LTI platform'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignment',
            name='resource_id',
            field=models.CharField(default='non', help_text='Canvas ID for the assignment resource', max_length=120),
            preserve_default=False,
        ),
    ]