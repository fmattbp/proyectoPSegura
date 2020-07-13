from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
import json
import servicios_back_end.system_monitor as system_monitor

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def monitor(request):
	if request.method == 'GET':
		datos_raw = system_monitor.get_info()
	datos = json.loads(datos_raw)
	return Response(datos)

