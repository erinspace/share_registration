from dateutil.parser import parse
from django.shortcuts import render, redirect

from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework_bulk import ListBulkCreateAPIView
from django.views.decorators.clickjacking import xframe_options_exempt

from push_endpoint.models import PushedData, Provider
from push_endpoint.serializers import UserSerializer
from push_endpoint.permissions import IsOwnerOrReadOnly
from push_endpoint.serializers import PushedDataSerializer


class DataList(ListBulkCreateAPIView):
    """
    List all pushed data, or push to the API.

    Note: This endpoint acts as a staging area for SHARE data. It will not show up in the main
    SHARE API data list until the data from your provider has been checked and pulled into SHARE.
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

        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')

        if from_date:
            filter['collectionDateTime__gte'] = parse(from_date)

        if to_date:
            filter['collectionDateTime__lte'] = parse(to_date)

        queryset = queryset.filter(**filter)

        return queryset


class EstablishedDataList(ListBulkCreateAPIView):
    """
    List all pushed data that comes from an established provider.

    Example query: pushed_data/established?from=2015-03-16&to=2015-04-06

    Note: If your data shows up in this list, it will be pulled into SHARE when the data is harvested.
    """
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(source=self.request.user)

    def get_queryset(self):
        queryset = PushedData.fetch_established()
        filter = {}

        from_date = self.request.QUERY_PARAMS.get('from')
        to_date = self.request.QUERY_PARAMS.get('to')

        if from_date:
            filter['collectionDateTime__gte'] = parse(from_date)

        if to_date:
            filter['collectionDateTime__lte'] = parse(to_date)

        queryset = queryset.filter(**filter)

        return queryset


class DataDetail(generics.RetrieveAPIView):
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


def render_api_form(request):
    token = request.user.auth_token
    return render(
        request,
        'rest_framework/get_api_key.html',
        {'auth_token': token}
    )


@xframe_options_exempt
def render_api_help(request):
    return render(
        request,
        'rest_framework/api_docs.html',
    )


@xframe_options_exempt
def gather_provider_information(request):
    user = request.user

    if request.method == 'POST':
        longname = request.POST.get('longname')
        shortname = request.POST.get('shortname')
        url = request.POST.get('url')

        try:
            provider_obj = Provider.objects.get(user=user)
        except Provider.DoesNotExist:
            provider_obj = Provider.objects.create(user=user)

        provider_obj.longname = longname
        provider_obj.shortname = shortname
        provider_obj.url = url

        provider_obj.save()

    return redirect('/provider_information/')


@xframe_options_exempt
def provider_information(request):
    user = request.user

    provider_details = Provider.objects.get(user=user)

    url = provider_details.url
    shortname = provider_details.shortname
    longname = provider_details.longname
    token = request.user.auth_token

    return render(
        request,
        'registration/preferences.html',
        {'request': request, 'shortname': shortname, 'longname': longname, 'url': url, 'auth_token': token}
    )
