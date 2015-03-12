from django.db import models


class PushedData(models.Model):
    source = models.ForeignKey('auth.User', related_name='data')
    description = models.TextField()
    contributors = models.TextField()
    tags = models.TextField()
    title = models.TextField()
    dateUpdated = models.DateField()
    url = models.URLField()
    serviceID = models.TextField()
    doi = models.TextField()
