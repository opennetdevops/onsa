# Generated by Django 2.0.7 on 2018-11-07 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jeangrey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='customer_location',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='jeangrey.CustomerLocation'),
            preserve_default=False,
        ),
    ]