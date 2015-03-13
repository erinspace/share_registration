from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer

from push_endpoint.models import PushedData
from push_endpoint.validators import ValidDOI


class PushedDataSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    source = serializers.ReadOnlyField(source='source.username')

    class Meta:
        model = PushedData
        fields = ('id', 'description', 'contributors', 'tags', 'source',
                  'title', 'dateUpdated', 'url', 'serviceID', 'doi', 'source')
        list_serializer_class = BulkListSerializer

        validators = [
            ValidDOI()
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'data')
