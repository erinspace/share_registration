import datetime

from django.db import models
from django.utils import timezone


class RegistrationInfo(models.Model):

    # Basic Information
    provider_short_name = models.CharField(max_length=50, primary_key=True)
    provider_long_name = models.CharField(max_length=100)
    base_url = models.URLField()
    description = models.TextField()
    oai_provider = models.BooleanField()

    # Terms of Service and Metadata Permissions Questions
    meta_tos = models.BooleanField()
    meta_privacy = models.BooleanField()
    meta_sharing_tos = models.BooleanField()
    meta_license = models.CharField(max_length=100)
    meta_license_extended = models.BooleanField()
    meta_future_license = models.BooleanField()

    # OAI Harvester Information
    property_list = models.TextField()
    approved_sets = models.TextField()
    registration_date = models.DateTimeField('date registered')

    def __unicode__(self):
        return self.provider_short_name

    def was_registered_recently(self, days=1):
        return self.registration_date >= timezone.now() - datetime.timedelta(days)

    was_registered_recently.admin_order_field = 'registration_date'
    was_registered_recently.boolean = True
    was_registered_recently.short_description = 'Registered recently?'
