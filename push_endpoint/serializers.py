from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer

from push_endpoint.models import PushedData, Provider
from push_endpoint.validators import JsonSchema


class PushedDataSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    source = serializers.ReadOnlyField(source='source.username')

    class Meta:
        model = PushedData
        fields = ('id', 'collectionDateTime', 'source', 'jsonData')
        list_serializer_class = BulkListSerializer

        validators = [
            JsonSchema()
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'data')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'longname', 'shortname', 'url', 'favicon_dataurl')
