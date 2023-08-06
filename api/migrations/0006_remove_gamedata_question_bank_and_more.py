# Generated by Django 4.2 on 2023-07-16 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_gamedata_question_bank_alter_gamedata_assignment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedata',
            name='question_bank',
        ),
        migrations.AlterField(
            model_name='gamedata',
            name='assignment',
            field=models.ForeignKey(default=999999999, help_text='Relation to corresponding assignment', on_delete=django.db.models.deletion.CASCADE, related_name='related_assignment', to='api.assignment'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.JSONField()),
                ('question_bank', models.ForeignKey(help_text='Relation to corresponding bank', on_delete=django.db.models.deletion.CASCADE, to='api.questionbank')),
            ],
        ),
    ]