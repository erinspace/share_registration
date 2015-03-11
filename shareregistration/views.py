from django.shortcuts import render
# from rest_framework.reverse import reverse
# from rest_framework.response import Response


def index(request):
    return render(request, 'index.html')
