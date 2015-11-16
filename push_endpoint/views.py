import json
import base64
from six.moves import urllib_parse
from dateutil.parser import parse
from django.shortcuts import render, redirect

from rest_framework import generics
from rest_framework import permissions
from rest_framework_bulk import ListBulkCreateAPIView
from django.views.decorators.clickjacking import xframe_options_exempt

from push_endpoint.forms import ProviderForm
from push_endpoint.models import PushedData, Provider
from push_endpoint.permissions import IsOwnerOrReadOnly
from push_endpoint.serializers import PushedDataSerializer, ProviderSerializer


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

        updated_from = self.request.query_params.get('from')
        updated_to = self.request.query_params.get('to')

        if updated_from:
            filter['updated__gte'] = parse(updated_from)
        if updated_to:
            filter['updated__lte'] = parse(updated_to)

        queryset = queryset.filter(**filter)
        for data in queryset:
            data.jsonData = json.dumps(data.jsonData)
        return queryset


class EstablishedDataList(generics.ListAPIView):
    """
    List all pushed data that comes from an established provider.

    Example query: pushed_data/established?from=2015-03-16&to=2015-04-06

    Note: If your data shows up in this list, it will be pulled into SHARE when the data is harvested.
    """
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_queryset(self):
        queryset = PushedData.fetch_established()
        filter = {}

        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')

        if from_date:
            filter['updated__gte'] = parse(from_date)

        if to_date:
            filter['updated__lte'] = parse(to_date)

        queryset = queryset.filter(**filter)
        for data in queryset:
            data.jsonData = json.dumps(data.jsonData)

        return queryset


class DataDetail(generics.RetrieveAPIView):
    """
    Retrieve pushed data
    """
    queryset = PushedData.objects.all()
    serializer_class = PushedDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class ProviderList(generics.ListAPIView):
    """
    List all providers and their information.
    """
    serializer_class = ProviderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Provider.objects.filter(established=True)
        return queryset


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
def render_settings(request):
    user = request.user
    provider_obj = Provider.objects.get(user=user)

    longname = provider_obj.longname
    shortname = provider_obj.shortname
    url = provider_obj.url
    token = request.user.auth_token

    return render(
        request,
        'registration/information.html', {
            'longname': longname,
            'shortname': shortname,
            'url': url,
            'token': token
        }
    )


@xframe_options_exempt
def provider_information(request):
    user = request.user
    url = None
    shortname = None
    longname = None
    favicon = None
    form = None

    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES)
        longname = request.POST.get('longname')
        url = request.POST.get('url')
        favicon = request.FILES.get('favicon_image')
        if form.is_valid():
            try:
                provider_obj = Provider.objects.get(user=user)
            except Provider.DoesNotExist:
                provider_obj = Provider.objects.create(user=user)

            url_list = url.split('.')
            shortname = url_list[-2].replace('http://', '').replace('https://', '')

            if favicon:
                provider_obj.favicon = favicon
                favicon_binary = provider_obj.favicon.read()
                provider_obj.favicon_dataurl = 'data:image/png;base64,' + urllib_parse.quote(base64.encodestring(favicon_binary))

            provider_obj.longname = longname
            provider_obj.shortname = shortname
            provider_obj.url = url
            provider_obj.save()

            return redirect('render_settings')

    try:
        Provider.objects.get(user=user)
    except Provider.DoesNotExist:
        form = ProviderForm(form)
        return render(
            request,
            'registration/gather_information.html', {
            'request': request,
            'form': form
            }
        )
    return redirect('render_settings')
