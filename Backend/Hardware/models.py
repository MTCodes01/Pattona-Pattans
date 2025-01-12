from django.db import models

class HardwareInitialization(models.Model):
    """Model to store the data needed for the hardware initialization"""
    device_id = models.IntegerField()
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255)
    device_ip = models.GenericIPAddressField()
    device_port = models.IntegerField()
    device_api_key = models.CharField(max_length=255)

    class Meta:
        db_table = 'hardware_initialization'

class RealTimeData(models.Model):
    """Model to store the real-time data from the hardware"""
    device_id = models.IntegerField()
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255)
    current = models.FloatField()
    voltage = models.FloatField()
    wattage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'real_time_data'

class HistoricalData(models.Model):
    """Model to store the historical data from the hardware"""
    device_id = models.IntegerField()
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255)
    current = models.FloatField()
    voltage = models.FloatField()
    wattage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historical_data'

class HardwareStatus(models.Model):
    """Model to store the status of the hardware"""
    device_id = models.IntegerField()
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hardware_status'

