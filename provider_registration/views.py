from datetime import date, timedelta

import requests
from lxml import etree

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render

from provider_registration.models import RegistrationInfo
from provider_registration.forms import ProviderForm, InitialProviderForm

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
    """ Shows initial provider form
    """
    form = InitialProviderForm()
    return render(
        request,
        'provider_registration/initial_registration_form.html',
        {'form': form}
    )


def save_provider_info(provider_name, base_url):
    """ Makes 2 requests to the provided base URL:
        1 for the sets available
        1 for the list of properties
        The sets available are added as multiple selections for the next form,
        the properties are pre-loaded into the properties field.
    """

    # request 1 for the setSpecs available
    set_url = base_url + '?verb=ListSets'
    set_data_request = requests.get(set_url)
    all_content = etree.XML(set_data_request.content)
    set_names = all_content.xpath('//oai_dc:setSpec/node()', namespaces=NAMESPACES)
    set_names = [name.replace('publication:', '') for name in set_names]

    # request 2 for records 10 days back just in case
    start_date = str(date.today() - timedelta(10))
    prop_url = base_url + '?verb=ListRecords&metadataPrefix=oai_dc&from={}T00:00:00Z'.format(start_date)
    prop_data_request = requests.get(prop_url)
    all_prop_content = etree.XML(prop_data_request.content)
    pre_names = all_prop_content.xpath('//ns0:metadata', namespaces=NAMESPACES)[0].getchildren()[0].getchildren()
    all_names = [name.tag.replace('{' + NAMESPACES['dc'] + '}', '') for name in pre_names]
    property_names = list(set([name for name in all_names if name not in BASE_SCHEMA]))

    # check to see if provider with that name exists
    try:
        RegistrationInfo.objects.get(provider_name=provider_name)
        # TODO - fix this
        print('{} already exists'.format(provider_name))
        return None
        # return render(request, 'provider_registration/already_exists.html', {'provider': provider_name})
    except ObjectDoesNotExist:
        print('SAVING {}'.format(provider_name))
        RegistrationInfo(
            provider_name=provider_name,
            base_url=base_url,
            property_list=property_names,
            approved_sets=set_names,
            registration_date=timezone.now()
        ).save()


def register_provider(request):
    if request.method == 'POST':
        if request.path == u'/provider_registration/self_register':
            name = request.POST['provider_name']
            url = request.POST['base_url']
            save_provider_info(name, url)
            pre_saved_data = RegistrationInfo.objects.get(provider_name=name)

            form = ProviderForm(
                {
                    'provider_name': name,
                    'base_url': url,
                    'approved_sets': pre_saved_data.approved_sets,
                    'property_list': pre_saved_data.property_list
                }
            )

            return render(
                request,
                'provider_registration/self_registration_form.html',
                {'form': form}
            )
        else:
            print('Now Updating data!')
            form_data = ProviderForm(request.POST)
            form_data.is_valid()  # TODO - fix this
            form_data = form_data.clean()

            object_to_update = RegistrationInfo.objects.get(provider_name=form_data['provider_name'])

            object_to_update.property_list = form_data['property_list']
            object_to_update.approved_sets = form_data['approved_sets']

            object_to_update.save()

            return render(
                request,
                'provider_registration/confirmation.html',
                {'provider': form_data['provider_name']}
            )
