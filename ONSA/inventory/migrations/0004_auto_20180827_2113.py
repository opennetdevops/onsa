# Generated by Django 2.0.7 on 2018-08-27 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20180823_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientnodeport',
            name='deviceType',
        ),
        migrations.RemoveField(
            model_name='clientnodeport',
            name='location',
        ),
        migrations.RemoveField(
            model_name='clientnodeport',
            name='mgmtIP',
        ),
        migrations.RemoveField(
            model_name='clientnodeport',
            name='model',
        ),
        migrations.RemoveField(
            model_name='clientnodeport',
            name='name',
        ),
        migrations.RemoveField(
            model_name='clientnodeport',
            name='vendor',
        ),
    ]