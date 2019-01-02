# Generated by Django 2.0.7 on 2018-08-14 16:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0009_remove_task_strategy'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='parameters',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]
