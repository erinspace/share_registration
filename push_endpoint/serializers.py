import json

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer

from push_endpoint.models import PushedData, Provider
from push_endpoint.validators import JsonSchema


class PushedDataSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    source = serializers.ReadOnlyField(source='source.username')
    docID = serializers.ReadOnlyField()

    class Meta:
        model = PushedData
        fields = ('id', 'collectionDateTime', 'docID', 'source', 'jsonData')
        list_serializer_class = BulkListSerializer

        validators = [
            JsonSchema()
        ]

    def create(self, validated_data):
        json_text = validated_data.get('jsonData').replace("u'", '"').replace("'", '"')
        json_data = json.loads(json_text)

        json_data['shareProperties'] = {
            'source': validated_data['source'].username,
            'docID': json_data['uris']['providerUris'][0]
        }

        validated_data['jsonData'] = json_data
        validated_data['docID'] = json_data['uris']['providerUris'][0]
        return PushedData.objects.create(**validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'data')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'longname', 'shortname', 'url', 'favicon_dataurl')
