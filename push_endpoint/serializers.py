# from django.forms import widgets

from django.contrib.auth.models import User
from rest_framework import serializers
from push_endpoint.models import PushedData


class PushedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushedData
        fields = ('id', 'description', 'contributors', 'tags', 'source',
                  'title', 'dateUpdated', 'url', 'serviceID', 'doi')


class UserSerializer(serializers.ModelSerializer):
    data = serializers.PrimaryKeyRelatedField(many=True, queryset=PushedData.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'data')
