# Generated by Django 2.0.1 on 2018-01-29 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_spider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, default='gxrc.com', max_length=255, null=True)),
                ('href', models.TextField()),
                ('uuid', models.CharField(max_length=100, unique=True)),
                ('jab_name', models.CharField(max_length=255)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('place', models.CharField(blank=True, max_length=255, null=True)),
                ('update', models.CharField(blank=True, max_length=255, null=True)),
                ('number', models.CharField(blank=True, max_length=255, null=True)),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('experience', models.CharField(blank=True, max_length=255, null=True)),
                ('nature', models.CharField(blank=True, max_length=255, null=True)),
                ('welfare', models.TextField()),
                ('job_info', models.TextField()),
                ('company_info', models.TextField()),
                ('company_address', models.TextField()),
                ('job_keywords', models.TextField()),
                ('company_keywords', models.TextField()),
            ],
        ),
    ]
