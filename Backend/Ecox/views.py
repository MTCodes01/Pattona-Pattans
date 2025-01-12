from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import models
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


class InitializationAPI(APIView):
    """
    API for initializing the system's User -> House -> Room -> Device hierarchy.
    """
    def post(self, request):
        try:
            # Step 1: Create a User
            user, user_created = models.User.objects.get_or_create(
                username="sim_user",
                defaults={
                    "email": "sim_user@example.com",
                    "password": "password123"  # Note: This should be hashed
                }
            )

            # Step 2: Create a House
            house, house_created = models.House.objects.get_or_create(
                house_name="Simulated House",
                defaults={
                    "address": "123 Simulated St",
                    "username": user
                }
            )

            # Step 3: Create Rooms
            room_names = ["Living Room", "Bedroom", "Kitchen"]
            rooms = []
            for name in room_names:
                room, room_created = models.Room.objects.get_or_create(
                    room_name=name,
                    house=house
                )
                rooms.append(room)

            # Step 4: Create Devices
            devices = []
            for room in rooms:
                for i in range(1, 4):  # Create 3 devices per room
                    device, device_created = models.Device.objects.get_or_create(
                        device_type="Simulated Device",
                        room=room,
                        defaults={
                            "state": False,
                            "power": 0.0,
                            "status": "offline",
                            "schedule_enabled": False
                        }
                    )
                    devices.append(device)

            return Response({
                'message': 'System initialization complete',
                'user': {'id': user.id, 'username': user.username},
                'house': {'id': house.house_id, 'name': house.house_name},
                'rooms': [{'id': room.room_id, 'name': room.room_name} for room in rooms],
                'devices': [{'id': device.device_id, 'type': device.device_type, 'room': device.room.room_name} for device in devices]
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HomeHierarchyAPI(APIView):
    def get(self, request, username):
        try:
            # Step 1: Fetch houses linked to the user
            UserModel = models.User
            user = UserModel.objects.filter(username=username).first()
            if not user:
                return Response({"error": "User not found"}, status=404)

            HouseModel = models.House
            houses = HouseModel.objects.filter(username_id=user.id)
            if not houses.exists():
                return Response({"error": "No houses found for the user"}, status=404)

            result = []

            for house in houses:
                house_data = {
                    "name": house.house_name,
                    "type": "Home",
                    "children": []
                }

                # Step 2: Fetch rooms for the house
                RoomModel = models.Room
                rooms = RoomModel.objects.filter(house_id=house.id)
                for room in rooms:
                    room_data = {
                        "name": room.room_name,
                        "type": "Room",
                        "children": []
                    }

                    # Step 3: Fetch devices in the room
                    DeviceModel = models.Device
                    devices = DeviceModel.objects.filter(room_id=room.id)
                    for device in devices:
                        # Step 4: Check device status
                        DeviceStatusModel = models.DeviceStatus
                        status_entry = DeviceStatusModel.objects.filter(device_id=device.id).first()
                        if status_entry:
                            status = status_entry.status
                        else:
                            # Fetch latest usage if no status exists
                            EnergyUsageModel = models.EnergyUsage
                            latest_usage = EnergyUsageModel.objects.filter(device_id=device.id).order_by("-timestamp").first()
                            status = "Unknown"  # Default status
                            if latest_usage:
                                # Example logic to determine status
                                status = "On" if latest_usage.power > 0 else "Off"

                                # Update device status
                                DeviceStatusModel.objects.update_or_create(
                                    device_id=device.id,
                                    defaults={"status": status}
                                )

                        room_data["children"].append({
                            "name": device.device_name,
                            "type": device.device_type,
                            "status": status,
                            "schedule": []  # Add schedule details if needed
                        })

                    house_data["children"].append(room_data)

                result.append(house_data)

            return Response(result, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class DatabaseExplorerAPI(APIView):
    """
    API to display all tables and their contents.
    """
    def get(self, request):
        try:
            data = {}

            # Step 1: Get all tables in the database
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
                tables = [row[0] for row in cursor.fetchall()]

            data['tables'] = {}

            # Step 2: For each table, get its columns and rows
            for table_name in tables:
                # Get columns
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}'")
                    columns = [row[0] for row in cursor.fetchall()]

                # Get rows
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                data['tables'][table_name] = {
                    'columns': columns,
                    'rows': rows
                }

            return Response(data, status=status.HTTP_200_OK, content_type="application/json")

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")

    def get_model_class(self, table_name):
        """
        Utility method to get the model class for a given table name.
        """
        try:
            for model in models.get_models():
                if model._meta.db_table == table_name:
                    return model
        except Exception:
            pass
        return None
    
class UsageAPI(APIView):
    def get(self, request):
        energy_usage_data = list(models.EnergyUsage.objects.values())
        return Response(energy_usage_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data  # Expecting {current, voltage, wattage, time_count}
        try:
            models.EnergyUsage.objects.create(**data)
            return Response({'message': 'Usage data added'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SwitchAPI(APIView):
    def get(self, request):
        try:
            switch_data = models.Switch.objects.first()
            if switch_data:
                return Response({'state': switch_data.state, 'power_controls': switch_data.power_controls}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Switch data not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data  # Expecting {state, power_controls}
        try:
            switch_data, created = models.Switch.objects.get_or_create(id=1, defaults=data)
            if not created:
                for key, value in data.items():
                    setattr(switch_data, key, value)
                switch_data.save()
            return Response({'message': 'Switch state updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class DeviceStatusAPI(APIView):
    def get(self, request):
        try:
            device_statuses = list(models.DeviceStatus.objects.values())
            return Response(device_statuses, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotificationsAPI(APIView):
    def get(self, request):
        try:
            notifications = list(models.Notification.objects.values())
            return Response(notifications, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        notification = request.data  # Expecting {alert_type, message}
        try:
            models.Notification.objects.create(**notification)
            return Response({'message': 'Notification created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsAPI(APIView):
    def get(self, request):
        try:
            energy_usage_data = list(models.EnergyUsage.objects.values())
            return Response({'energy_usage': energy_usage_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SchedulesAPI(APIView):
    def get(self, request):
        try:
            schedules = list(models.Schedule.objects.values())
            return Response({'schedules': schedules}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        schedule_data = request.data  # Expecting {time, action}
        try:
            models.Schedule.objects.create(**schedule_data)
            return Response({'message': 'Schedule created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, schedule_id):
        try:
            schedule = models.Schedule.objects.get(id=schedule_id)
            schedule.delete()
            return Response({'message': f'Schedule {schedule_id} deleted'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'error': f'Schedule with ID {schedule_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({"success": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    return render(request, 'login.html')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Check if the username already exists
            if models.User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists."}, status=400)

            # Create a new user
            user = models.User.objects.create_user(username=username, email=email, password=password)

            return JsonResponse({"success": "User created successfully"}, status=201)

        except Exception as e:
            print(f"Error in signup view: {e}")
            return JsonResponse({"error": "An error occurred during sign-up."}, status=500)
    return render(request, 'Signup.html')

