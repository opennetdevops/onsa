# Generated by Django 2.0.7 on 2018-08-29 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180829_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpeport',
            name='cpe',
        ),
        migrations.RemoveField(
            model_name='cpeport',
            name='services',
        ),
        migrations.AlterUniqueTogether(
            name='servicecperelations',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='servicecperelations',
            name='cpe_port',
        ),
        migrations.RemoveField(
            model_name='servicecperelations',
            name='service',
        ),
        migrations.AddField(
            model_name='service',
            name='client_node_port',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='service',
            name='client_node_sn',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.DeleteModel(
            name='Cpe',
        ),
        migrations.DeleteModel(
            name='CpePort',
        ),
        migrations.DeleteModel(
            name='ServiceCpeRelations',
        ),
    ]
