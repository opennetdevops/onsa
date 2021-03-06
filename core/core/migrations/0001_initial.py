# Generated by Django 2.0.7 on 2018-08-21 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cpe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('ip_management', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CpePort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('cpe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Cpe')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(max_length=50, unique=True)),
                ('product_identifier', models.CharField(max_length=50)),
                ('bandwidth', models.PositiveSmallIntegerField()),
                ('vrf', models.CharField(blank=True, max_length=50)),
                ('prefix', models.CharField(blank=True, max_length=50)),
                ('public_network', models.CharField(blank=True, max_length=50)),
                ('service_type', models.CharField(choices=[('vcpe_irs', 'vcpe_irs'), ('MPLS', 'MPLS'), ('VPLS', 'VPLS'), ('cpeless_irs', 'cpeless_irs')], default='cpeless_irs', max_length=30)),
                ('service_state', models.CharField(choices=[('PENDING', 'PENDING'), ('REQUESTED', 'REQUESTED'), ('COMPLETED', 'COMPLETED'), ('ERROR', 'ERROR')], default='PENDING', max_length=15)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Client')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCpeRelations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=50)),
                ('client_node_sn', models.CharField(max_length=50)),
                ('client_node_port', models.CharField(max_length=50)),
                ('bandwidth', models.CharField(blank=True, max_length=50)),
                ('prefix', models.CharField(blank=True, max_length=50)),
                ('vrf', models.CharField(blank=True, max_length=50)),
                ('service_state', models.CharField(blank=True, max_length=50)),
                ('service_identifier', models.CharField(blank=True, max_length=50)),
                ('service_type', models.CharField(blank=True, max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Client')),
                ('cpe_port', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.CpePort')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Service')),
            ],
        ),
        migrations.AddField(
            model_name='cpeport',
            name='services',
            field=models.ManyToManyField(blank=True, through='core.ServiceCpeRelations', to='core.Service'),
        ),
        migrations.CreateModel(
            name='CpeLessIrsService',
            fields=[
            ],
            options={
                'indexes': [],
                'proxy': True,
            },
            bases=('core.service',),
        ),
        migrations.CreateModel(
            name='MplsService',
            fields=[
            ],
            options={
                'indexes': [],
                'proxy': True,
            },
            bases=('core.service',),
        ),
        migrations.CreateModel(
            name='VcpePublicIrsService',
            fields=[
            ],
            options={
                'indexes': [],
                'proxy': True,
            },
            bases=('core.service',),
        ),
        migrations.AlterUniqueTogether(
            name='servicecperelations',
            unique_together={('cpe_port', 'service')},
        ),
    ]
