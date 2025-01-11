from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Example data storage (replace with actual hardware communication)
HARDWARE_STATUS = {'id': 1, 'status': 'Online', 'battery': '80%'}
REAL_TIME_DATA = {'sensor_type': 'Voltage', 'value': '220V'}
HISTORICAL_DATA = []

# Class for Initializing Hardware Connection
class HardwareInitializationAPI(APIView):
    def post(self, request):
        data = request.data  # Expecting {hardware_id, protocol, parameters}
        # Perform initialization logic here
        return Response({'message': f"Hardware {data['hardware_id']} initialized"}, status=status.HTTP_201_CREATED)


# Class for Retrieving Real-Time Sensor Data
class RealTimeDataAPI(APIView):
    def get(self, request):
        return Response(REAL_TIME_DATA, status=status.HTTP_200_OK)


# Class for Retrieving Historical Sensor Data
class HistoricalDataAPI(APIView):
    def get(self, request):
        return Response(HISTORICAL_DATA, status=status.HTTP_200_OK)


# Class for Checking Hardware Status
class HardwareStatusAPI(APIView):
    def get(self, request):
        return Response(HARDWARE_STATUS, status=status.HTTP_200_OK)


# Class for Stopping Hardware Connection
class HardwareStopConnectionAPI(APIView):
    def post(self, request):
        hardware_id = request.data.get('hardware_id')  # Expecting {hardware_id}
        # Perform hardware disconnection logic here
        return Response({'message': f"Hardware {hardware_id} stopped"}, status=status.HTTP_200_OK)
