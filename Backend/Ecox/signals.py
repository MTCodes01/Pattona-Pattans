from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from datetime import datetime
from .models import DeviceUsage, RoomUsage, HouseUsage  # Import the models from Ecox app

@receiver(post_save, sender=DeviceUsage)
def update_room_usage(sender, instance, created, **kwargs):
    if created:
        # Get all device usage data for the room
        device_usages = DeviceUsage.objects.filter(
            device__room=instance.device.room,
            timestamp__date=instance.timestamp.date()
        ).aggregate(
            total_current=Sum('current'),
            total_voltage=Sum('voltage'),
            total_wattage=Sum('wattage')
        )

        # Create or update room usage
        RoomUsage.objects.create(
            room=instance.device.room,
            total_current=device_usages['total_current'] or 0,
            total_voltage=device_usages['total_voltage'] or 0,
            total_wattage=device_usages['total_wattage'] or 0
        )

@receiver(post_save, sender=RoomUsage)
def update_house_usage(sender, instance, created, **kwargs):
    if created:
        # Get all room usage data for the house
        room_usages = RoomUsage.objects.filter(
            room__house=instance.room.house,
            timestamp__date=instance.timestamp.date()
        ).aggregate(
            total_current=Sum('total_current'),
            total_voltage=Sum('total_voltage'),
            total_wattage=Sum('total_wattage')
        )

        # Create or update house usage
        HouseUsage.objects.create(
            house=instance.room.house,
            total_current=room_usages['total_current'] or 0,
            total_voltage=room_usages['total_voltage'] or 0,
            total_wattage=room_usages['total_wattage'] or 0
        )