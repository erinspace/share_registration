## custom validators
from rest_framework import serializers

import requests


class ValidDOI:

    def __call__(self, value):

        doi_url = 'http://dx.doi.org/'

        doi = value.get('doi')

        if doi_url in doi:
            request_url = doi
        else:
            request_url = doi_url + doi

        response = requests.get(request_url)
        print(request_url)
        print(response.status_code)

        if response.status_code == 404:
            raise serializers.ValidationError('DOI does not resolve, please enter a valid DOI')
