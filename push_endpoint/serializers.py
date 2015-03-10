# from django.forms import widgets
from rest_framework import serializers
from push_endpoint.models import PushedData


class PushedDataSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    data = serializers.TextField()

    def create(self, validated_data):
        return PushedData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance
