# Generated by Django 2.0.7 on 2018-10-31 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charles', '0003_auto_20181025_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='target_state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
