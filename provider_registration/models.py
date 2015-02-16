import datetime

from django.db import models
from django.utils import timezone


class RegistrationInfo(models.Model):

    provider_name = models.CharField(max_length=100, primary_key=True)
    base_url = models.CharField(max_length=100)
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
