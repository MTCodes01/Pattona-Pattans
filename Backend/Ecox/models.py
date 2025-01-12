from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    house_ids = ArrayField(models.IntegerField(), blank=True, default=list)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='ecox_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='ecox_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

class House(models.Model):
    house_id = models.AutoField(primary_key=True)
    house_name = models.CharField(max_length=255)
    address = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room_count = models.IntegerField(default=0)
    device_count = models.IntegerField(default=0)
    room_ids = ArrayField(models.IntegerField(), blank=True, default=list)

    class Meta:
        db_table = 'houses'

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=255)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device_count = models.IntegerField(default=0)
    device_ids = ArrayField(models.IntegerField(), blank=True, default=list)

    class Meta:
        db_table = 'rooms'

class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    device_type = models.CharField(max_length=50)
    state = models.BooleanField(default=False)
    power = models.FloatField(default=0)
    status = models.CharField(max_length=50, default='offline')
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule_enabled = models.BooleanField(default=False)
    schedule = models.JSONField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = 'devices'

class DeviceUsage(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    current = models.FloatField()
    voltage = models.FloatField()
    wattage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'device_usage'

class RoomUsage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    total_current = models.FloatField()
    total_voltage = models.FloatField()
    total_wattage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'room_usage'

class HouseUsage(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    total_current = models.FloatField()
    total_voltage = models.FloatField()
    total_wattage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'house_usage'

class EnergyUsage(models.Model):
    current = models.FloatField(help_text="The current (in Amps) of the energy usage measurement")
    voltage = models.FloatField(help_text="The voltage (in Volts) of the energy usage measurement")
    wattage = models.FloatField(help_text="The wattage (in Watts) of the energy usage measurement")
    time_count = models.IntegerField(help_text="The time count (in seconds) of the energy usage measurement")

    class Meta:
        db_table = 'energy_usage'

class Switch(models.Model):
    state = models.BooleanField(default=False, help_text="The current state of the switch (ON/OFF)")
    power_controls = models.CharField(max_length=15, help_text="The power control settings of the switch (e.g., 'dim' or 'bright')")

    class Meta:
        db_table = 'switches'

class DeviceStatus(models.Model):
    device_id = models.IntegerField()
    status = models.CharField(max_length=15)

    class Meta:
        db_table = 'devicestatus'

class Notification(models.Model):
    alert_type = models.CharField(max_length=15)
    message = models.CharField(max_length=255)

    class Meta:
        db_table = 'notifications'

class Schedule(models.Model):
    time = models.TimeField()
    action = models.CharField(max_length=15)

    class Meta:
        db_table = 'schedules'

