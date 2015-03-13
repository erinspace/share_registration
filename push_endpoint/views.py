from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

from dateutil.parser import parse

from push_endpoint.models import PushedData
from push_endpoint.serializers import UserSerializer
from push_endpoint.permissions import IsOwnerOrReadOnly
from push_endpoint.serializers import PushedDataSerializer

from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView


class DataList(ListBulkCreateUpdateDestroyAPIView):
    """
    List all pushed data, or push to the API
    """
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    ordering_fields = ('dateUpdated')

    def perform_create(self, serializer):
        serializer.save(source=self.request.user)

    def get_queryset(self):
        """ Return queryset based on from and to kwargs
        """
        filter = {}
        queryset = PushedData.objects.all()

        start_date = self.request.QUERY_PARAMS.get('from', None)
        end_date = self.request.QUERY_PARAMS.get('to', None)

        if start_date is not None:
            filter['dateUpdated__gte'] = parse(start_date)

        if end_date is not None:
            filter['dateUpdated__lte'] = parse(end_date)

        queryset = queryset.filter(**filter)

        return queryset


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete pushed data
    """
    queryset = PushedData.objects.all()
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'data': reverse('data-list', request=request, format=format)
    })
