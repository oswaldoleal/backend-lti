# Generated by Django 4.1.2 on 2023-02-19 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lti1p3_tool_config', '0002_alter_ltitool_id_alter_ltitoolkey_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, help_text='Internal deployment ID', primary_key=True, serialize=False)),
                ('lti_deployment_id', models.CharField(help_text='LTI Deployment ID', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='LTIUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, help_text='LTI User ID', primary_key=True, serialize=False)),
                ('lti_user_id', models.UUIDField(help_text='User sub as refered by the LTI platform')),
                ('name', models.CharField(blank=True, help_text='User name in LTI platform', max_length=50)),
                ('email', models.EmailField(help_text='User email in the LTI platform', max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(auto_created=True, null=True)),
                ('email', models.EmailField(help_text='User email', max_length=254, unique=True)),
                ('password', models.CharField(help_text='User password', max_length=512)),
                ('ltiConfig', models.ForeignKey(help_text='Relation to corresponding tool deployment on an LTI Platform', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ltiConfig', to='lti1p3_tool_config.ltitool')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('register_date', models.DateTimeField(auto_created=True, help_text='Timestamp when the course first appeared in our system')),
                ('id', models.BigIntegerField(auto_created=True, help_text='LTI Course ID', primary_key=True, serialize=False)),
                ('lti_resource_id', models.CharField(help_text='LTI resource ID from the LTI platform', max_length=40, unique=True)),
                ('name', models.CharField(help_text='LTI Course name', max_length=120)),
                ('deployment', models.ForeignKey(help_text='Relation to corresponding tool deployment on an LTI Platform', on_delete=django.db.models.deletion.CASCADE, related_name='deployment', to='api.deployment')),
            ],
        ),
    ]
