# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-03 16:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20180703_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vlantag',
            name='used',
        ),
    ]