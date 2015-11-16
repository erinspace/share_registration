import collections

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from jsonfield import JSONField


class Provider(models.Model):
    user = models.OneToOneField(User)
    established = models.BooleanField(default=False)
    url = models.URLField(max_length=255, null=True)
    shortname = models.CharField(max_length=50, null=True)
    longname = models.CharField(max_length=255, null=True, verbose_name="Name")
    favicon_image = models.ImageField(upload_to='shareregistration/static/img/favicons', null=True, blank=True)
    favicon_dataurl = models.TextField(null=True, verbose_name="Favicon Data URL")


class PushedData(models.Model):
    jsonData = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    docID = models.TextField()
    provider = models.ForeignKey(Provider, related_name='data')
    source = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, default='created')

    @property
    def established(self):
        return self.source.provider.established

    @classmethod
    def fetch_established(cls):
        return cls.objects.all().filter(source__provider__established=True)

    class Meta:
        verbose_name = 'Data Object'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
