# Generated by Django 2.2.13 on 2020-09-12 16:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0004_auto_20200912_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistReport',
            fields=[
                ('dReportId', models.CharField(blank=True, max_length=32, primary_key=True, serialize=False, verbose_name='Report Id')),
                ('reportingMonth', models.CharField(blank=True, choices=[('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=2, verbose_name='Month')),
                ('reportingYear', models.CharField(blank=True, max_length=4, verbose_name='Year')),
                ('districtRole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.DistrictRole')),
            ],
            options={
                'verbose_name': 'District Report',
                'verbose_name_plural': 'District Reports',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskId', models.AutoField(primary_key=True, serialize=False)),
                ('taskText', models.CharField(blank=True, max_length=100, verbose_name='Task')),
                ('taskPoolStatus', models.BooleanField(blank=True, default=True, null=True, verbose_name='Task Pool Status')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('responseId', models.AutoField(primary_key=True, serialize=False)),
                ('completionStatus', models.CharField(blank=True, choices=[('0', 'Incomplete'), ('1', 'Partially Complete'), ('2', 'Complete')], max_length=2, verbose_name='Completion Status')),
                ('response', models.TextField(blank=True, verbose_name='Response')),
                ('driveLink', models.CharField(blank=True, max_length=100, verbose_name='Drive Link')),
                ('modifiedOn', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Modified on')),
                ('dReport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DistReport.DistReport')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DistReport.Task')),
            ],
        ),
    ]
