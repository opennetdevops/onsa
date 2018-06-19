# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-19 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nsx', '0021_hub_uplink_pg_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CpeLessIrsService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edge_name', models.CharField(max_length=50)),
                ('product_identifier', models.CharField(max_length=50)),
                ('ip_wan', models.CharField(max_length=50)),
                ('sco_logical_unit', models.PositiveSmallIntegerField()),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nsx.Client')),
                ('portgroup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nsx.Portgroup')),
                ('public_network', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nsx.IpPublicSegment')),
                ('sco_port', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nsx.ScoPort')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]