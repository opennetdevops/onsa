# Generated by Django 2.0.7 on 2019-05-30 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jeangrey', '0006_tip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='gts',
            new_name='gts_id',
        ),
    ]