# Generated by Django 2.0.7 on 2018-09-03 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20180903_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientnodeport',
            name='uplink_port',
        ),
        migrations.AddField(
            model_name='clientnode',
            name='uplink_port',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]