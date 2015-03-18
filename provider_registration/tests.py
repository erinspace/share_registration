import vcr
import datetime

from django.utils import timezone
from django.test import TestCase
# from django.core.urlresolvers import reverse

from provider_registration.models import RegistrationInfo
from provider_registration.forms import InitialProviderForm


# def create_registration(provider_long_name, base_url, days):
#     date = timezone.now() + datetime.timedelta(days=days)
#     RegistrationInfo.objects.create(
#         provider_long_name=provider_long_name,
#         base_url=base_url,
#         registration_date=date)


class RegistrationMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = RegistrationInfo(registration_date=time)
        self.assertEqual(future_question.was_registered_recently(), False)


class RegistrationFormTests(TestCase):

    @vcr.use_cassette('provider_registration/vcr_cassettes/oai_response.yaml')
    def test_valid_oai_data(self):
        form = InitialProviderForm({
            'contact_name': 'BubbaRay Dudley',
            'contact_email': 'BullyRay@dudleyboyz.net',
            'provider_long_name': 'Devon - Get the Tables',
            'base_url': 'http://repository.stcloudstate.edu/do/oai/',
            'description': 'A description',
            'oai_provider': True,
            'meta_license': 'MIT'
        })
        self.assertTrue(form.is_valid())

    @vcr.use_cassette('provider_registration/vcr_cassettes/other_response.yaml')
    def test_valid_other_data(self):
        form = InitialProviderForm({
            'contact_name': 'BubbaRay Dudley',
            'contact_email': 'BullyRay@dudleyboyz.net',
            'provider_long_name': 'Devon - Get the Tables',
            'base_url': 'http://wwe.com',
            'description': 'A description',
            'oai_provider': False,
            'meta_license': 'MIT'
        })
        self.assertTrue(form.is_valid())
