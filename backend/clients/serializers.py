from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.Serializer):
    class Meta:
        model = Client
        fields = '__all__'
