# Generated by Django 2.2.13 on 2020-09-16 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_auto_20200909_0138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='date_joined',
        ),
    ]
