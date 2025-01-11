from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
import datetime

# Class for Initializing Hardware Connection
class HardwareInitializationAPI(APIView):
    def post(self, request):
        data = request.data  # Expecting {hardware_id, protocol, parameters}
        hardware_status, created = models.HardwareStatus.objects.get_or_create(
            hardware_id=data['hardware_id'],
            defaults={'protocol': data['protocol'], 'parameters': data['parameters']}
        )
        if not created:
            hardware_status.protocol = data['protocol']
            hardware_status.parameters = data['parameters']
            hardware_status.save()
        return Response({'message': f"Hardware {data['hardware_id']} initialized"}, status=status.HTTP_201_CREATED)

class RealTimeDataAPI(APIView):
    def post(self, request):
        data = request.data  # Expecting {device_id, current, voltage, wattage}
        try:
            device = models.Device.objects.get(device_id=data['device_id'])
            
            # Update device status
            device.power = data['wattage']
            device.status = 'online'
            device.last_updated = datetime.now()
            device.save()
            
            # Create device usage record
            models.DeviceUsage.objects.create(
                device=device,
                current=data['current'],
                voltage=data['voltage'],
                wattage=data['wattage']
            )
            
            return Response({'message': 'Data recorded successfully'}, status=status.HTTP_201_CREATED)
        except models.Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Class for Retrieving Historical Sensor Data
class HistoricalDataAPI(APIView):
    def get(self, request):
        data = models.HistoricalData.objects.all()
        if data:
            historical_data_list = [{'id': item.id, 'sensor_type': item.sensor_type, 'value': item.value, 'timestamp': item.timestamp} for item in data]
            return Response(historical_data_list, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No historical data available'}, status=status.HTTP_404_NOT_FOUND)


# Class for Checking Hardware Status
class HardwareStatusAPI(APIView):
    def get(self, request):
        hardware_status = models.HardwareStatus.objects.last()
        if hardware_status:
            return Response({'id': hardware_status.hardware_id, 'status': hardware_status.status, 'battery': hardware_status.battery}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hardware status available'}, status=status.HTTP_404_NOT_FOUND)


# Class for Stopping Hardware Connection
class HardwareStopConnectionAPI(APIView):
    def post(self, request):
        hardware_id = request.data.get('hardware_id')  # Expecting {hardware_id}
        try:
            hardware_status = models.HardwareStatus.objects.get(hardware_id=hardware_id)
            hardware_status.status = 'Offline'
            hardware_status.save()
            return Response({'message': f"Hardware {hardware_id} stopped"}, status=status.HTTP_200_OK)
        except models.HardwareStatus.DoesNotExist:
            return Response({'message': f"Hardware {hardware_id} not found"}, status=status.HTTP_404_NOT_FOUND)

