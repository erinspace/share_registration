# from django.forms import widgets

from django.contrib.auth.models import User
from rest_framework import serializers
from push_endpoint.models import PushedData

from push_endpoint.validators import ValidDOI


class PushedDataSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.ReadOnlyField(source='source.username')

    class Meta:
        model = PushedData
        fields = ('id', 'description', 'contributors', 'tags', 'source',
                  'title', 'dateUpdated', 'url', 'serviceID', 'doi', 'source')

        validators = [
            ValidDOI()
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'data')
