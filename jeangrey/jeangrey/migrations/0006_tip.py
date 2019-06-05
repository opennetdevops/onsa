# Generated by Django 2.0.7 on 2019-05-29 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jeangrey', '0005_service_gts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jeangrey.Service')),
            ],
            options={
                'abstract': False,
            },
            bases=('jeangrey.service',),
        ),
    ]