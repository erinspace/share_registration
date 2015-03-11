from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

from push_endpoint.models import PushedData
from push_endpoint.serializers import PushedDataSerializer
from push_endpoint.serializers import UserSerializer


class DataList(generics.ListCreateAPIView):
    """
    List all pushed data, or push to the API
    """
    queryset = PushedData.objects.all()
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete pushed data
    """
    queryset = PushedData.objects.all()
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
