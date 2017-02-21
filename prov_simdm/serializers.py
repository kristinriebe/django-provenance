from rest_framework import serializers


class ProtocolSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=200)
    #version = serializers.CharField(max_length=200)

