# Generated by Django 2.0.7 on 2018-10-30 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeangrey', '0005_auto_20181026_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='prefix',
        ),
        migrations.AddField(
            model_name='cpeirs',
            name='prefix',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cpelessirs',
            name='prefix',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vcpeirs',
            name='prefix',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vcpeirs',
            name='public_network',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
