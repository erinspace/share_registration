from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class Provider(models.Model):
    user = models.OneToOneField(User)
    established = models.BooleanField(default=False)


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

    @property
    def established(self):
        return self.source.provider.established

    @classmethod
    def fetch_established(cls):
        test = cls.objects.all().filter(source__provider__established=True)
        return test
        # return cls.objects.find(source__provider__established=True)

    class Meta:
        verbose_name = 'Data Object'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
