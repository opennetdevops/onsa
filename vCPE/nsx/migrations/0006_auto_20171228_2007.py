# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nsx', '0005_auto_20171228_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpPublicSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used', models.BooleanField(default=False)),
                ('ip', models.GenericIPAddressField()),
                ('mask', models.PositiveSmallIntegerField()),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nsx.Hub')),
            ],
        ),
        migrations.RemoveField(
            model_name='ipwan',
            name='mask',
        ),
    ]
