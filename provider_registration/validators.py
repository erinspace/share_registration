import requests
from lxml import etree

from django import forms

IDENTIFY = '?verb=Identify'

NAMESPACES = {'oai': 'http://www.openarchives.org/OAI/2.0/'}


class URLResolves(object):
    def __call__(self, value):
        ''' value is the serialized data to be validated '''
        try:
            data = requests.get(value)
        except requests.exceptions.ConnectionError:
            raise forms.ValidationError('URL does not resolve, please enter  a valid URL')
        if data.status_code == 404:
            raise forms.ValidationError('URL does not resolve, please enter  a valid URL')


class ValidOAIURL(object):
    def __call__(self, value):
        ''' value is the serialized data to be validated '''

        url = value + IDENTIFY

        data = requests.get(url)
        if data.status_code == 404:
            raise forms.ValidationError('URL does not resolve, please enter  a valid URL')

        try:
            doc = etree.XML(data.content)
        except etree.XMLSyntaxError:
            raise forms.ValidationError('URL does not return valid XML, please enter a valid OAI-PMH url')

        repository_name = doc.xpath('//oai:repositoryName/node()', namespaces=NAMESPACES) or ['']
        if not repository_name[0]:
            raise forms.ValidationError(
                'XML Does not appear to point to a valid OAI-PMH source, please enter a valid OAI-PMH url'
            )
