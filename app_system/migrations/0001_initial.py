# Generated by Django 2.0.2 on 2018-05-31 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSSConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_ip', models.CharField(max_length=190)),
                ('system_name', models.CharField(max_length=190)),
                ('system_pass', models.CharField(max_length=190)),
                ('ss_port', models.IntegerField()),
                ('ss_pass', models.CharField(max_length=190)),
                ('is_share', models.BooleanField(default=False)),
                ('error_times', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
