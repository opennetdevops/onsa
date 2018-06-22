# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-22 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180622_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpelessirsservice',
            name='hub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Hub'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cpelessmplsservice',
            name='hub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Hub'),
            preserve_default=False,
        ),
    ]
