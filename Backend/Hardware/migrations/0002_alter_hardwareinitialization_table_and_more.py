# Generated by Django 5.1.4 on 2025-01-12 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hardware', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='hardwareinitialization',
            table='hardware_initialization',
        ),
        migrations.AlterModelTable(
            name='hardwarestatus',
            table='hardware_status',
        ),
        migrations.AlterModelTable(
            name='historicaldata',
            table='historical_data',
        ),
        migrations.AlterModelTable(
            name='realtimedata',
            table='real_time_data',
        ),
    ]
