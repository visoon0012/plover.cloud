# Generated by Django 2.0.1 on 2018-01-29 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_spider', '0002_job'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='jab_name',
            new_name='job_name',
        ),
    ]
