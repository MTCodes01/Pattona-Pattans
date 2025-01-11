from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import EnergyUsage, Switch, DeviceStatus, Notification, Schedule
from django.core.exceptions import ObjectDoesNotExist


class UsageAPI(APIView):
    def get(self, request):
        energy_usage_data = list(EnergyUsage.objects.values())
        return Response(energy_usage_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data  # Expecting {current, voltage, wattage, time_count}
        try:
            EnergyUsage.objects.create(**data)
            return Response({'message': 'Usage data added'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SwitchAPI(APIView):
    def get(self, request):
        try:
            switch_data = Switch.objects.first()
            if switch_data:
                return Response({'state': switch_data.state, 'power_controls': switch_data.power_controls}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Switch data not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data  # Expecting {state, power_controls}
        try:
            switch_data, created = Switch.objects.get_or_create(id=1, defaults=data)
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
            device_statuses = list(DeviceStatus.objects.values())
            return Response(device_statuses, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotificationsAPI(APIView):
    def get(self, request):
        try:
            notifications = list(Notification.objects.values())
            return Response(notifications, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        notification = request.data  # Expecting {alert_type, message}
        try:
            Notification.objects.create(**notification)
            return Response({'message': 'Notification created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsAPI(APIView):
    def get(self, request):
        try:
            energy_usage_data = list(EnergyUsage.objects.values())
            return Response({'energy_usage': energy_usage_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SchedulesAPI(APIView):
    def get(self, request):
        try:
            schedules = list(Schedule.objects.values())
            return Response({'schedules': schedules}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        schedule_data = request.data  # Expecting {time, action}
        try:
            Schedule.objects.create(**schedule_data)
            return Response({'message': 'Schedule created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, schedule_id):
        try:
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.delete()
            return Response({'message': f'Schedule {schedule_id} deleted'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'error': f'Schedule with ID {schedule_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def index(request):
    return render(request, 'index.html')
