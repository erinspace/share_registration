from datetime import date, timedelta

import requests
from lxml import etree

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render

from provider_registration.forms import ProviderForm, InitialProviderForm
from provider_registration.models import RegistrationInfo

NAMESPACES = {'dc': 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/',
              'ns0': 'http://www.openarchives.org/OAI/2.0/'}
BASE_SCHEMA = ['title', 'contributor', 'creator', 'subject', 'description']


def index(request):
    latest_provider_list = RegistrationInfo.objects.order_by('registration_date')

    context = {'latest_provider_list': latest_provider_list}

    return render(request, 'provider_registration/index.html', context)


def detail(request, provider_name):
    provider = get_object_or_404(RegistrationInfo, provider_name=provider_name)
    return render(
        request,
        'provider_registration/detail.html',
        {'provider': provider}
    )


def get_provider_info(request):
    """ Makes 2 requests to the provided base URL:
            1 for the sets available
            1 for the list of properties
        The sets available are added as multiple selections for the next form,
        the properties are pre-loaded into the properties field.
    """
    if request.method == 'POST':
        form_data = InitialProviderForm(request.POST)
        form_data.is_valid()  # TODO - fix this
        form_data = form_data.clean()

        # request 1 for the setSpecs available
        set_url = form_data['base_url'] + '?verb=ListSets'
        set_data_request = requests.get(set_url)
        all_content = etree.XML(set_data_request.content)
        set_names = all_content.xpath('//oai_dc:setSpec/node()', namespaces=NAMESPACES)
        set_names = [name.replace('publication:', '') for name in set_names]

        # request 2 for records 10 days back just in case
        start_date = str(date.today() - timedelta(10))
        prop_url = form_data['base_url'] + '?verb=ListRecords&metadataPrefix=oai_dc&from={}T00:00:00Z'.format(start_date)
        prop_data_request = requests.get(prop_url)
        all_prop_content = etree.XML(prop_data_request.content)
        pre_names = all_prop_content.xpath('//ns0:metadata', namespaces=NAMESPACES)[0].getchildren()[0].getchildren()
        all_names = [name.tag.replace('{' + NAMESPACES['dc'] + '}', '') for name in pre_names]
        property_names = list(set([name for name in all_names if name not in BASE_SCHEMA]))

        return {'set_names': set_names, 'property_names': property_names}

    else:
        form = InitialProviderForm()
        return render(
            request,
            'provider_registration/initial_registration_form.html',
            {'form': form}
        )


def register_provider(request):
    if request.method == 'POST':
        form_data = ProviderForm(request.POST)
        form_data.is_valid()  # TODO - fix this
        form_data = form_data.clean()

        # check to see if provider with that name exists
        try:
            RegistrationInfo.objects.get(provider_name=form_data['provider_name'])
            return render(request, 'provider_registration/already_exists.html', {'provider': form_data['provider_name']})
        except ObjectDoesNotExist:
            RegistrationInfo(
                provider_name=form_data['provider_name'],
                base_url=form_data['base_url'],
                property_list=form_data['property_list'],
                approved_sets=form_data['approved_sets'],
                registration_date=timezone.now()
            ).save()

            return render(
                request,
                'provider_registration/confirmation.html',
                {'provider': form_data['provider_name']}
            )
    else:
        pre_populated_data = get_provider_info(request)
        import ipdb; ipdb.set_trace()
        form = ProviderForm()
        return render(
            request,
            'provider_registration/self_registration_form.html',
            {'form': form}
        )
