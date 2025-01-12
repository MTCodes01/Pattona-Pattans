# Hardware/tests/test_models.py
from django.test import TestCase
from .models import HardwareStatus, RealTimeData, HistoricalData

class HardwareStatusTest(TestCase):
    def setUp(self):
        self.hardware_status = HardwareStatus.objects.create(
            device_id=1,
            device_name='Test Device',
            device_type='Light',
            status='online'
        )

    def test_hardware_status_creation(self):
        self.assertEqual(self.hardware_status.device_id, 1)
        self.assertEqual(self.hardware_status.device_name, 'Test Device')
        self.assertEqual(self.hardware_status.device_type, 'Light')

class RealTimeDataTest(TestCase):
    def setUp(self):
        self.realtime_data = RealTimeData.objects.create(
            device_id=1,
            device_name='Test Device',
            device_type='Light',
            current=1.0,
            voltage=220.0,
            wattage=220.0
        )

    def test_realtime_data_creation(self):
        self.assertEqual(self.realtime_data.device_id, 1)
        self.assertEqual(self.realtime_data.current, 1.0)
        self.assertEqual(self.realtime_data.voltage, 220.0)
        self.assertEqual(self.realtime_data.wattage, 220.0)