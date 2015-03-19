from django.db import models


class PushedData(models.Model):
    url = models.URLField()
    doi = models.TextField()
    tags = models.TextField(blank=True)
    title = models.TextField()
    serviceID = models.TextField()
    description = models.TextField(blank=True)
    contributors = models.TextField()
    dateUpdated = models.DateField(auto_now_add=True)
    source = models.ForeignKey('auth.User', related_name='data')
