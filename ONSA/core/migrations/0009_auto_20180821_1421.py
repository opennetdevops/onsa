# Generated by Django 2.0.7 on 2018-08-21 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180821_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicecperelations',
            name='client_name',
        ),
        migrations.AlterField(
            model_name='servicecperelations',
            name='client',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
