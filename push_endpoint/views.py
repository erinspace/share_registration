from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

from dateutil.parser import parse

from push_endpoint.models import PushedData
from push_endpoint.serializers import UserSerializer
from push_endpoint.permissions import IsOwnerOrReadOnly
from push_endpoint.serializers import PushedDataSerializer

from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from rest_framework import views
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from . import negotiators, parsers, utils


class DataList(ListBulkCreateUpdateDestroyAPIView):
    """
    List all pushed data, or push to the API
    """
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(source=self.request.user)

    def get_queryset(self):
        """ Return queryset based on from and to kwargs
        """
        filter = {}
        queryset = PushedData.objects.all()

        from_date = self.request.QUERY_PARAMS.get('from')
        to_date = self.request.QUERY_PARAMS.get('to')

        if from_date:
            filter['dateUpdated__gte'] = parse(from_date)

        if to_date:
            filter['dateUpdated__lte'] = parse(to_date)

        queryset = queryset.filter(**filter)

        return queryset


class EstablishedDataList(ListBulkCreateUpdateDestroyAPIView):
    """
    List all pushed data that comes from an established provider
    """
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(source=self.request.user)

    def get_queryset(self):
        return PushedData.fetch_established()


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


class ProductView(views.APIView):

    parser_classes = (parsers.JSONSchemaParser,)
    content_negotiation_class = negotiators.IgnoreClientContentNegotiation

    def post(self, request, *args, **kwargs):
        try:
            # implicitly calls parser_classes
            request.DATA
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.message),
                status=status.HTTP_400_BAD_REQUEST
            )
        utils.store_the_json(request.DATA)
        return Response()
