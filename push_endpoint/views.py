from rest_framework import status
# from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from push_endpoint.models import PushedData
from push_endpoint.serializers import PushedDataSerializer


@api_view(['GET', 'POST'])
def data_list(request, format=None):
    """
    List all pushed data, or push to the API
    """
    if request.method == 'GET':
        data_objects = PushedData.objects.all()
        serializer = PushedDataSerializer(data_objects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PushedDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def data_detail(request, pk, format=None):
    """
    Retrieve, update or delete pushed data
    """
    try:
        pushed_objects = PushedData.objects.get(pk=pk)
    except PushedData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PushedDataSerializer(pushed_objects)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PushedDataSerializer(pushed_objects, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pushed_objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
