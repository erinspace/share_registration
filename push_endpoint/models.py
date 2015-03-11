from django.db import models


class PushedData(models.Model):
    owner = models.ForeignKey('auth.User', related_name='push_endpoint')
    description = models.TextField()
    contributors = models.TextField()
    tags = models.TextField()
    source = models.TextField()
    title = models.TextField()
    dateUpdated = models.TextField()
    url = models.TextField()
    serviceID = models.TextField()
    doi = models.TextField()
