# Generated by Django 2.2.13 on 2020-09-30 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0007_districtrole_distrolesname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='distLogo',
            field=models.ImageField(null=True, upload_to='distLogos', verbose_name='District Logo'),
        ),
        migrations.AlterField(
            model_name='districtcouncil',
            name='tenureEnds',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Tenure ends on'),
        ),
        migrations.AlterField(
            model_name='districtcouncil',
            name='tenureStarts',
            field=models.DateTimeField(null=True, verbose_name='Tenure starts on'),
        ),
    ]
