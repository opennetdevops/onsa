# Generated by Django 2.0.7 on 2018-09-07 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20180907_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='bandwidth',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='client_node_port',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='client_node_sn',
            field=models.CharField(max_length=50, null=True),
        ),
    ]