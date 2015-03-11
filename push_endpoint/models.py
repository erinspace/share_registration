from django.db import models


class PushedData(models.Model):
    description = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    contributors = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    tags = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    source = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    title = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    dateUpdated = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    url = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    serviceID = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
    doi = models.TextField()  # TODO: make this a json field or seperate for each in normed data?
