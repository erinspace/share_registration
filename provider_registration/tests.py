import vcr
import datetime
import requests

from django.utils import timezone
from django.test import TestCase

from provider_registration import views
from provider_registration.models import RegistrationInfo
from provider_registration.forms import InitialProviderForm, OAIProviderForm


class RegistrationMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = RegistrationInfo(registration_date=time)
        self.assertEqual(future_question.was_registered_recently(), False)

    def test_unicode_name(self):
        time = timezone.now() + datetime.timedelta(days=30)
        registraion = RegistrationInfo(
            provider_long_name='SquaredCircle Digest',
            registration_date=time
        )
        self.assertEqual(unicode(registraion), 'SquaredCircle Digest')


class RegistrationFormTests(TestCase):

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response.yaml')
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

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/other_response.yaml')
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

    def test_misformed_url(self):
        form = InitialProviderForm({
            'contact_name': 'BubbaRay Dudley',
            'contact_email': 'BullyRay@dudleyboyz.net',
            'provider_long_name': 'Devon - Get the Tables',
            'base_url': 'DEVONGETTHETABLLESSSSSS',
            'description': 'A description',
            'oai_provider': False,
            'meta_license': 'MIT'
        })
        with self.assertRaises(requests.exceptions.MissingSchema):
            form.is_valid()

    def test_formed_not_valid(self):
        form = InitialProviderForm({
            'contact_name': 'BubbaRay Dudley',
            'contact_email': 'BullyRay@dudleyboyz.net',
            'provider_long_name': 'Devon - Get the Tables',
            'base_url': 'http://notreallyaurul.nope',
            'description': 'A description',
            'oai_provider': False,
            'meta_license': 'MIT'
        })
        self.assertFalse(form.is_valid())

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response.yaml')
    def test_missing_contact_name(self):
        form = InitialProviderForm({
            'contact_name': '',
            'contact_email': 'BullyRay@dudleyboyz.net',
            'provider_long_name': 'Devon - Get the Tables',
            'base_url': 'http://repository.stcloudstate.edu/do/oai/',
            'description': 'A description',
            'oai_provider': True,
            'meta_license': 'MIT'
        })
        self.assertFalse(form.is_valid())

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response.yaml')
    def test_missing_contact_email(self):
        form = InitialProviderForm({
            'contact_name': 'Spike Dudley',
            'contact_email': '',
            'provider_long_name': 'Devon - Get the Tables',
            'base_url': 'http://repository.stcloudstate.edu/do/oai/',
            'description': 'A description',
            'oai_provider': True,
            'meta_license': 'MIT'
        })
        self.assertFalse(form.is_valid())

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response.yaml')
    def test_malformed_contact_email(self):
        form = InitialProviderForm({
            'contact_name': 'Spike Dudley',
            'contact_email': 'email',
            'provider_long_name': 'Devon - Get the Tables',
            'base_url': 'http://repository.stcloudstate.edu/do/oai/',
            'description': 'A description',
            'oai_provider': True,
            'meta_license': 'MIT'
        })
        self.assertFalse(form.is_valid())

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response.yaml')
    def test_missing_provider_name(self):
        form = InitialProviderForm({
            'contact_name': 'Spike Dudley',
            'contact_email': 'email@email.com',
            'provider_long_name': '',
            'base_url': 'http://repository.stcloudstate.edu/do/oai/',
            'description': 'A description',
            'oai_provider': True,
            'meta_license': 'MIT'
        })
        self.assertFalse(form.is_valid())


class TestOAIProviderForm(TestCase):

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response.yaml')
    def test_valid_oai_data(self):
        approved_set_set = [('totally', 'approved')]
        form = OAIProviderForm({
            'provider_long_name': 'SuperCena',
            'base_url': 'http://repository.stcloudstate.edu/do/oai/',
            'property_list': "some, properties",
            'approved_sets': ["totally"]
        }, choices=approved_set_set)
        self.assertTrue(form.is_valid())


class ViewMethodTests(TestCase):

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response_listsets.yaml')
    def test_valid_oai_url(self):
        provider_long_name = 'Stardust Weekly'
        base_url = 'http://repository.stcloudstate.edu/do/oai/'
        success = views.save_oai_info(provider_long_name, base_url)
        self.assertTrue(success['value'])
        self.assertEqual(success['reason'], 'Stardust Weekly registered and saved successfully')

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/other_response_oai.yaml')
    def test_invalid_oai_url(self):
        provider_long_name = 'Golddust Monthly'
        base_url = 'http://wwe.com'
        success = views.save_oai_info(provider_long_name, base_url)
        self.assertFalse(success['value'])
        self.assertEqual(success['reason'], 'XML Not Valid')

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/oai_response_listsets.yaml')
    def test_repeat_oai_name(self):
        RegistrationInfo(
            provider_long_name='Stardust Weekly',
            base_url='http://repository.stcloudstate.edu/do/oai/',
            property_list=['some', 'properties'],
            approved_sets=['some', 'sets'],
            registration_date=timezone.now()
        ).save()

        provider_long_name = 'Stardust Weekly'
        base_url = 'http://repository.stcloudstate.edu/do/oai/'
        success = views.save_oai_info(provider_long_name, base_url)

        self.assertFalse(success['value'])
        self.assertEqual(success['reason'], 'Provider name already exists')

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/other_response_oai.yaml')
    def test_save_other_provider(self):
        provider_long_name = 'The COSMIC KEEEEEY'
        base_url = 'http://wwe.com'
        success = views.save_other_info(provider_long_name, base_url)
        self.assertTrue(success)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/other_response_oai.yaml')
    def test_repeat_provider_fails(self):
        RegistrationInfo(
            provider_long_name='Stardust Weekly',
            base_url='http://wwe.com',
            property_list=['some', 'properties'],
            registration_date=timezone.now()
        ).save()
        success = views.save_other_info('Stardust Weekly', 'http://wwe.com')
        self.assertFalse(success)
