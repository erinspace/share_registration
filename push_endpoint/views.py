from rest_framework import generics
from push_endpoint.models import PushedData
from push_endpoint.serializers import PushedDataSerializer


class DataList(generics.ListCreateAPIView):
    """
    List all pushed data, or push to the API
    """
    queryset = PushedData.objects.all()
    serializer_class = PushedDataSerializer


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete pushed data
    """
    queryset = PushedData.objects.all()
    serializer_class = PushedDataSerializer
