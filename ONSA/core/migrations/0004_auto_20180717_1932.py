# Generated by Django 2.0.7 on 2018-07-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180705_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpelessirsservice',
            name='service_id',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mplsservice',
            name='service_id',
            field=models.CharField(default=2, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publicirsservice',
            name='service_id',
            field=models.CharField(default=3, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cpelessirsservice',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('REQUESTED', 'REQUESTED'), ('COMPLETED', 'COMPLETED'), ('ERROR', 'ERROR')], default='PENDING', max_length=15),
        ),
        migrations.AlterField(
            model_name='mplsservice',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('REQUESTED', 'REQUESTED'), ('COMPLETED', 'COMPLETED'), ('ERROR', 'ERROR')], default='PENDING', max_length=15),
        ),
        migrations.AlterField(
            model_name='publicirsservice',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('REQUESTED', 'REQUESTED'), ('COMPLETED', 'COMPLETED'), ('ERROR', 'ERROR')], default='PENDING', max_length=15),
        ),
    ]