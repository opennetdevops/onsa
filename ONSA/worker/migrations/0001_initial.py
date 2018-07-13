# Generated by Django 2.0.7 on 2018-07-13 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(max_length=50)),
                ('service_type', models.CharField(max_length=50)),
                ('service_state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_state', models.CharField(blank=True, default='Creating', max_length=50)),
                ('task_type', models.CharField(max_length=30)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worker.Service')),
            ],
        ),
        migrations.CreateModel(
            name='MxCpelessIrsTask',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('worker.task',),
        ),
        migrations.CreateModel(
            name='MxVcpeTask',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('worker.task',),
        ),
        migrations.CreateModel(
            name='NsxTask',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('worker.task',),
        ),
    ]
