from rest_framework import serializers
from servicios_back_end import models

class MonitorSerializer (serializers.Serializer):
	cpu = serializers.IntegerField()
	memoria = serializers.IntegerField()
	disco = serializers.IntegerField()
