# Generated by Django 2.0.7 on 2018-11-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeangrey', '0002_service_customer_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.CharField(default=None, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]