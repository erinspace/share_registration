import datetime

from django.db import models
from django.utils import timezone

YES_NO_CHOICES = (
    ('Y', 'yes'),
    ('N', 'no')
)


class RegistrationInfo(models.Model):

    # Basic Information
    provider_name = models.CharField(max_length=100, primary_key=True)
    base_url = models.URLField()
    description = models.TextField()

    # Terms of Service and Metadata Permissions Questions
    meta_tos = models.CharField(max_length=1, choices=YES_NO_CHOICES)
    meta_privacy = models.CharField(max_length=1, choices=YES_NO_CHOICES)
    meta_sharing_tos = models.CharField(max_length=1, choices=YES_NO_CHOICES)
    meta_license = models.CharField(max_length=100)
    meta_license_extended = models.CharField(max_length=1, choices=YES_NO_CHOICES)
    meta_future_license = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    # # Harvester Information
    property_list = models.TextField()
    approved_sets = models.TextField()
    registration_date = models.DateTimeField('date registered')

    def __unicode__(self):
        return self.provider_name

    def was_registered_recently(self):
        return self.registration_date >= timezone.now() - datetime.timedelta(days=1)

    was_registered_recently.admin_order_field = 'registration_date'
    was_registered_recently.boolean = True
    was_registered_recently.short_description = 'Registered recently?'
