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


class PushedData(models.Model):
    jsonData = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    source = models.ForeignKey('auth.User', related_name='data')
    collectionDateTime = models.DateTimeField(auto_now_add=True)

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
