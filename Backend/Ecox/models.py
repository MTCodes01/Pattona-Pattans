from django.db import models

class EnergyUsage(models.Model):
    current = models.FloatField(help_text="The current (in Amps) of the energy usage measurement")
    voltage = models.FloatField(help_text="The voltage (in Volts) of the energy usage measurement")
    wattage = models.FloatField(help_text="The wattage (in Watts) of the energy usage measurement")
    time_count = models.IntegerField(help_text="The time count (in seconds) of the energy usage measurement")

class Switch(models.Model):
    state = models.BooleanField(default=False, help_text="The current state of the switch (ON/OFF)")
    power_controls = models.CharField(max_length=15, help_text="The power control settings of the switch (e.g., 'dim' or 'bright')")

class DeviceStatus(models.Model):
    device_id = models.IntegerField()
    status = models.CharField(max_length=15)

class Notification(models.Model):
    alert_type = models.CharField(max_length=15)
    message = models.CharField(max_length=255)

class Schedule(models.Model):
    time = models.TimeField()
    action = models.CharField(max_length=15)

