from django.db import models


class PushedData(models.Model):
    data = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
