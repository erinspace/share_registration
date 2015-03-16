import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from provider_registration.models import RegistrationInfo


def create_registration(provider_long_name, base_url, days):
    date = timezone.now() + datetime.timedelta(days=days)
    RegistrationInfo.objects.create(
        provider_long_name=provider_long_name,
        base_url=base_url,
        registration_date=date)


class RegistrationMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = RegistrationInfo(registration_date=time)
        self.assertEqual(future_question.was_registered_recently(), False)

    def test_invalid_url_throws_error(self):
        url = 'Not a real url'
        create_registration(
            provider_long_name='A Real Name',
            base_url=url,
            days=1)

    def test_not_selecting_oai_box_does_not_parse_xml(self):
        pass

    def test_blank_long_name_throws_error(self):
        create_registration(
            provider_long_name='',
            base_url='http://aurl.com',
            days=1)
        response = self.client.get(reverse('provider_registration:index'))
        self.assertQuerysetEqual(
            response.context['latest_provider_list'],
            ['<RegistrationInfo: >']
        )
