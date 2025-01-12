# Ecox/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import House, Room, Device, DeviceUsage, RoomUsage, HouseUsage

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            house_ids=[]  # Initialize empty ArrayField
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.house_ids, [])

class HouseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            house_ids=[]  # Initialize empty ArrayField
        )
        self.house = House.objects.create(
            house_name='Test House',
            address='123 Test St',
            username=self.user,
            room_ids=[]  # Initialize empty ArrayField
        )

    def test_house_creation(self):
        self.assertEqual(self.house.house_name, 'Test House')
        self.assertEqual(self.house.address, '123 Test St')
        self.assertEqual(self.house.username, self.user)
        self.assertEqual(self.house.room_ids, [])