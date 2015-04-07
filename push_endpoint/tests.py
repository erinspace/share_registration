import copy
import json

import vcr
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser, User
from push_endpoint.views import DataList, EstablishedDataList, render_api_help
from shareregistration.views import index as main_index


VALID_POST = {
    "jsonData":
    {
        "creationDate": "2014-09-12",
        "contributor": [
            {
                "name": "Roger Danger Ebert",
                "sameAs": [
                    "https://osf.io/wrgr2/"
                ],
                "familyName": "Ebert",
                "givenName": "Roger",
                "additionalName": "Danger",
                "email": "roger@example.com",
                "affiliation": "University of Movies"
            },
            {
                "name": "Roger Madness Ebert",
                "sameAs": [
                    "http://osf.io/wrgr3/"
                ],
                "familyName": "Ebert",
                "givenName": "Roger",
                "additionalName": "Madness",
                "email": "rogermadness@example.com",
                "affiliation": "University of Movies"
            }
        ],
        "language": "eng",
        "description": "This is a thing",
        "directLink": "https://www.example.com/stuff",
        "releaseDate": "2014-12-12",
        "freeToRead": {
        "startDate": "2014-09-12",
        "endDate": "2014-10-12"
        },
        "licenseRef": [
        {
            "uri": "http://www.mitlicense.com",
            "startDate": "2014-10-12",
            "endDate": "2014-11-12"
        }
        ],
        "notificationLink": "http://myresearch.com/",
        "publisher": "Roger Ebert Inc",
        "raw": "http://osf.io/raw/thisdocument/",
        "relation": [
        "http://otherresearch.com/this"
        ],
        "resourceIdentifier": "http://landingpage.com/this",
        "revisionTime": "2014-02-12T15:25:02Z",
        "source": "Big government",
        "sponsorship": [
        {
            "award": {
                "awardName": "Participation",
                "awardIdentifier": "http://example.com"
            },
            "sponsor": {
                "sponsorName": "Orange",
            "sponsorIdentifier": "http://example.com/orange"
            }
        }
        ],
        "title": "Interesting research",
        "journalArticleVersion": "AO",
        "versionOfRecord": "http://example.com/this/now/"
    }
}


class APIPostTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='bubbaray', password='dudley')

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi1.yaml')
    def test_valid_submission(self):
        view = DataList.as_view()
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(VALID_POST),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)

        self.assertEqual(response.status_code, 201)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi4.yaml')
    def test_established_view(self):
        view = EstablishedDataList.as_view()
        request = self.factory.post(
            '/pushed_data/established',
            json.dumps(VALID_POST),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_get_established_view(self):
        view = EstablishedDataList.as_view()
        request = self.factory.get(
            '/pushed_data/established'
        )
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_get_api_docs(self):
        view = render_api_help
        request = self.factory.get(
            '/help'
        )
        response = view(request)

        self.assertEqual(response.status_code, 200)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi.yaml')
    def test_missing_resourceIdentifier(self):
        view = DataList.as_view()
        invalid_post = copy.deepcopy(VALID_POST)
        invalid_post['jsonData'].pop('resourceIdentifier')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['detail'], "'resourceIdentifier' is a required property")
        self.assertEqual(response.status_code, 400)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi.yaml')
    def test_missing_title_fails(self):
        view = DataList.as_view()
        invalid_post = copy.deepcopy(VALID_POST)
        invalid_post['jsonData'].pop('title')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['detail'], "'title' is a required property")
        self.assertEqual(response.status_code, 400)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi.yaml')
    def test_missing_directLink_fails(self):
        view = DataList.as_view()
        invalid_post = copy.deepcopy(VALID_POST)
        invalid_post['jsonData'].pop('directLink')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['detail'], "'directLink' is a required property")
        self.assertEqual(response.status_code, 400)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi.yaml')
    def test_missing_contributors_fails(self):
        view = DataList.as_view()
        invalid_post = copy.deepcopy(VALID_POST)
        invalid_post['jsonData'].pop('contributor')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['detail'], "'contributor' is a required property")
        self.assertEqual(response.status_code, 400)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi3.yaml')
    def test_missing_raw(self):
        view = DataList.as_view()
        invalid_post = copy.deepcopy(VALID_POST)
        invalid_post['jsonData'].pop('raw')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['detail'], "'raw' is a required property")
        self.assertEqual(response.status_code, 400)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi4.yaml')
    def test_missing_description_is_ok(self):
        view = DataList.as_view()
        invalid_post = copy.deepcopy(VALID_POST)
        invalid_post['jsonData'].pop('description')
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(invalid_post),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)

        self.assertEqual(response.status_code, 201)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi.yaml')
    def test_anonomous_user_can_view(self):
        view = DataList.as_view()
        request = self.factory.get('/pushed_data/')
        request.user = AnonymousUser()
        response = view(request)

        self.assertEqual(response.status_code, 200)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi.yaml')
    def test_anonomous_user_can_not_post(self):
        view = DataList.as_view()
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(VALID_POST),
            content_type='application/json'
        )
        request.user = AnonymousUser()
        response = view(request)
        data = response.data

        self.assertEqual(data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 401)

    @vcr.use_cassette('provider_registration/test_utils/vcr_cassettes/doi2.yaml')
    def test_source_is_same_as_user(self):
        view = DataList.as_view()
        request = self.factory.post(
            '/pushed_data/',
            json.dumps(VALID_POST),
            content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        data = response.data

        self.assertEqual(data['source'], request.user.username)

    def test_render_index(self):
        view = main_index
        request = self.factory.get(
            '/index'
        )
        response = view(request)

        self.assertEqual(response.status_code, 200)
