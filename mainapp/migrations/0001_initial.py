# Generated by Django 3.2.5 on 2021-08-06 13:23

from django.db import migrations, models
import django.db.models.deletion
import mainapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('jobid', models.CharField(default=mainapp.models.generate_pk, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('check_terms', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobFile',
            fields=[
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mainapp.job')),
                ('file', models.FileField(upload_to=mainapp.models.job_directory_path)),
            ],
        ),
    ]
