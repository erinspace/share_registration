# from django.forms import widgets
from rest_framework import serializers
from push_endpoint.models import PushedData


class PushedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushedData
        fields = ('id', 'description', 'contributors', 'tags', 'source',
                  'title', 'dateUpdated', 'url', 'serviceID', 'doi')
