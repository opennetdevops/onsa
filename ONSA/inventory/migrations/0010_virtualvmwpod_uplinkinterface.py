# Generated by Django 2.0.7 on 2018-07-25 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_virtualvmwpod_routernode'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualvmwpod',
            name='uplinkInterface',
            field=models.CharField(max_length=50, null=True),
        ),
    ]