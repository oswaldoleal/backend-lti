# Generated by Django 4.2 on 2023-05-22 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='question_bank',
            field=models.ForeignKey(help_text='Relation to corresponding bank', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_bank', to='api.questionbank'),
        ),
    ]
