# Generated by Django 2.0.7 on 2018-10-30 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientnode',
            name='client',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clientnode',
            name='uplink_port',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]