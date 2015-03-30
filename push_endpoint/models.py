from django.db import models
from django.contrib.auth.models import User


class PushedData(models.Model):
    url = models.URLField()
    doi = models.TextField()
    title = models.TextField()
    serviceID = models.TextField()
    contributors = models.TextField()
    tags = models.TextField(blank=True)
    description = models.TextField(blank=True)
    dateUpdated = models.DateField(auto_now_add=True)
    source = models.ForeignKey('auth.User', related_name='data')

    class Meta:
        verbose_name = 'Data Object'


class Provider(models.Model):
    user = models.OneToOneField(User)
    established = models.BooleanField(default=False)
