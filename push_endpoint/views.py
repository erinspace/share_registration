from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from push_endpoint.models import PushedData
from push_endpoint.serializers import PushedDataSerializer


class DataList(APIView):
    """
    List all pushed data, or push to the API
    """

    def get(self, request, format=None):
        data_objects = PushedData.objects.all()
        serializer = PushedDataSerializer(data_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PushedDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataDetail(APIView):
    """
    Retrieve, update or delete pushed data
    """
    def get_object(self, pk):
        try:
            return PushedData.objects.get(pk=pk)
        except PushedData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pushed_objects = self.get_object(pk)
        serializer = PushedDataSerializer(pushed_objects)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pushed_object = self.get_object(pk)
        serializer = PushedDataSerializer(pushed_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pushed_object = self.get_object(pk)
        pushed_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
