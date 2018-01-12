# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 18:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nsx', '0009_auto_20171229_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='privateirsservice',
            name='portgroup',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='nsx.Portgroup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='privateirsservice',
            name='sco_port',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='nsx.ScoPort'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publicirsservice',
            name='portgroup',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='nsx.Portgroup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publicirsservice',
            name='sco_port',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='nsx.ScoPort'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='portgroup',
            name='vlan_tag',
            field=models.CharField(max_length=50),
        ),
    ]