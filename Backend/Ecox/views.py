from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

# Example data storage
ENERGY_USAGE_DATA = []
SWITCH_DATA = {'state': 'OFF', 'power': '50%'}
DEVICE_STATUSES = [{'id': 1, 'status': 'active'}]
NOTIFICATIONS = []

class UsageAPI(APIView):
    def get(self, request):
        return Response(ENERGY_USAGE_DATA, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data  # Expecting {current, voltage, wattage, time_count}
        ENERGY_USAGE_DATA.append(data)
        return Response({'message': 'Usage data added'}, status=status.HTTP_201_CREATED)


class SwitchAPI(APIView):
    def get(self, request):
        return Response({'data': SWITCH_DATA}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data  # Expecting {state, power}
        SWITCH_DATA.update(data)
        return Response({'message': 'Switch state updated'}, status=status.HTTP_200_OK)


class DeviceStatusAPI(APIView):
    def get(self, request):
        return Response(DEVICE_STATUSES, status=status.HTTP_200_OK)


class NotificationsAPI(APIView):
    def get(self, request):
        return Response(NOTIFICATIONS, status=status.HTTP_200_OK)

    def post(self, request):
        notification = request.data  # Expecting {alert_type, message}
        NOTIFICATIONS.append(notification)
        return Response({'message': 'Notification created'}, status=status.HTTP_201_CREATED)


class AnalyticsAPI(APIView):
    def get(self, request):
        return Response({'energy_usage': ENERGY_USAGE_DATA}, status=status.HTTP_200_OK)


class SchedulesAPI(APIView):
    def get(self, request):
        return Response({'schedules': []}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({'message': 'Schedule created'}, status=status.HTTP_201_CREATED)

    def delete(self, request, schedule_id):
        return Response({'message': f'Schedule {schedule_id} deleted'}, status=status.HTTP_204_NO_CONTENT)


def index(request):
    return render(request, 'index.html')
