# from django.forms import widgets

from django.contrib.auth.models import User
from rest_framework import serializers
from push_endpoint.models import PushedData


class PushedDataSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = PushedData
        fields = ('id', 'description', 'contributors', 'tags', 'source',
                  'title', 'dateUpdated', 'url', 'serviceID', 'doi', 'owner')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'data')
