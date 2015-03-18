import requests
from lxml import etree

from django import forms

IDENTIFY = '?verb=Identify'


class ValidOAIURL(object):
    def __call__(self, value):
        ''' value is the serialized data to be validated '''

        url = value.get('base_url' + IDENTIFY)

        data = requests.get(url)
        if data.status_code == 404:
            raise forms.ValidationError('Invalid OAI URL')

        doc = etree.XML(data.content)

        repository_name = doc.xpath('//repository_name/node()')

        print(repository_name)
