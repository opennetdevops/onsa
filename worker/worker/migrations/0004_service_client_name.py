# Generated by Django 2.0.7 on 2018-08-01 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0003_auto_20180730_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='client_name',
            field=models.CharField(default='None', max_length=50),
            preserve_default=False,
        ),
    ]
