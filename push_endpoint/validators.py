## custom validators
from rest_framework import serializers

import requests

DOI_URL = 'https://dx.doi.org/'


class ValidDOI(object):
    def __call__(self, value):
        ''' value is the serialized data to be validated '''

        doi = value.get('doi')

        if doi.startswith(DOI_URL):
            request_url = doi
        else:
            request_url = DOI_URL + doi

        response = requests.get(request_url)

        if response.status_code == 404:
            raise serializers.ValidationError('DOI does not resolve, please enter a valid DOI')
