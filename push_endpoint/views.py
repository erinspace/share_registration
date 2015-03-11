from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from push_endpoint.models import PushedData
from push_endpoint.serializers import PushedDataSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def data_list(request):
    """
    List all pushed data
    """
    if request.method == 'GET':
        data_objects = PushedData.objects.all()
        serializer = PushedDataSerializer(data_objects, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PushedDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def data_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        pushed_objects = PushedData.objects.get(pk=pk)
    except PushedData.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PushedDataSerializer(pushed_objects)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PushedDataSerializer(pushed_objects, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        pushed_objects.delete()
        return HttpResponse(status=204)
