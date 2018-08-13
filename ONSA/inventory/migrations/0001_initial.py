# Generated by Django 2.0.7 on 2018-08-13 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('deviceType', models.CharField(blank=True, max_length=50)),
                ('mgmtIP', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('uplinkInterface', models.CharField(max_length=50)),
                ('accessNodeId', models.CharField(max_length=4)),
                ('qinqOuterVlan', models.CharField(max_length=50)),
                ('logicalUnitId', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccessPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('port', models.CharField(max_length=50, null=True)),
                ('used', models.BooleanField(default=False)),
                ('client', models.CharField(blank=True, max_length=50, null=True)),
                ('accessNode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.AccessNode')),
            ],
        ),
        migrations.CreateModel(
            name='ClientNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('deviceType', models.CharField(blank=True, max_length=50)),
                ('mgmtIP', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('serialNumber', models.CharField(blank=True, max_length=50)),
                ('client', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LogicalUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logical_unit_id', models.PositiveSmallIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NsxEdge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('deviceType', models.CharField(blank=True, max_length=50)),
                ('mgmtIP', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('edgeName', models.CharField(max_length=50)),
                ('ipWan', models.CharField(max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpticalNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('deviceType', models.CharField(blank=True, max_length=50)),
                ('mgmtIP', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('serialNumber', models.CharField(blank=True, max_length=50)),
                ('client', models.CharField(blank=True, max_length=50)),
                ('hwId', models.CharField(blank=True, max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Portgroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vlan_tag', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('used', models.BooleanField(default=False)),
                ('dvportgroup_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RouterNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('deviceType', models.CharField(blank=True, max_length=50)),
                ('mgmtIP', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('privateWanIp', models.GenericIPAddressField(blank=True, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VirtualVmwPod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('deviceType', models.CharField(blank=True, max_length=50)),
                ('mgmtIP', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('uplinkInterface', models.CharField(max_length=50, null=True)),
                ('transportZoneName', models.CharField(blank=True, max_length=50)),
                ('clusterName', models.CharField(blank=True, max_length=50)),
                ('datastoreId', models.CharField(blank=True, max_length=50)),
                ('resourcePoolId', models.CharField(blank=True, max_length=50)),
                ('datacenterId', models.CharField(blank=True, max_length=50)),
                ('uplinkPg', models.CharField(blank=True, max_length=50)),
                ('uplinkPgId', models.CharField(blank=True, max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location')),
                ('routerNode', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.RouterNode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VlanTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vlan_tag', models.CharField(max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VlantagAccessports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceid', models.CharField(blank=True, max_length=50)),
                ('sn_client_node', models.CharField(max_length=50)),
                ('client_node_port', models.CharField(max_length=50)),
                ('bandwidth', models.CharField(max_length=50)),
                ('accessport', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.AccessPort')),
                ('vlantag', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.VlanTag')),
            ],
            options={
                'db_table': 'inventory_vlantag_accessPorts',
            },
        ),
        migrations.AddField(
            model_name='vlantag',
            name='accessPorts',
            field=models.ManyToManyField(blank=True, through='inventory.VlantagAccessports', to='inventory.AccessPort'),
        ),
        migrations.AddField(
            model_name='portgroup',
            name='virtualVmwPod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.VirtualVmwPod'),
        ),
        migrations.AddField(
            model_name='nsxedge',
            name='portgroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Portgroup'),
        ),
        migrations.AddField(
            model_name='logicalunit',
            name='routerNodes',
            field=models.ManyToManyField(blank=True, to='inventory.RouterNode'),
        ),
        migrations.AddField(
            model_name='clientnode',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location'),
        ),
        migrations.AddField(
            model_name='accessnode',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location'),
        ),
        migrations.AlterUniqueTogether(
            name='vlantagaccessports',
            unique_together={('vlantag', 'accessport')},
        ),
    ]
