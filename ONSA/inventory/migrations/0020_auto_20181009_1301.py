# Generated by Django 2.0.7 on 2018-10-09 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20181002_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='vlantag',
            new_name='vlan_tag',
        ),
        migrations.AlterUniqueTogether(
            name='products',
            unique_together={('vlan_tag', 'access_node', 'access_port_id')},
        ),
    ]
