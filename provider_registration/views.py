import requests
from lxml import etree
from datetime import date, timedelta

import logging

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, render_to_response

from provider_registration.models import RegistrationInfo
from provider_registration.forms import OAIProviderForm, OtherProviderForm, InitialProviderForm

logger = logging.getLogger(__name__)


NAMESPACES = {'dc': 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/',
              'ns0': 'http://www.openarchives.org/OAI/2.0/'}
BASE_SCHEMA = ['title', 'contributor', 'creator', 'subject', 'description']


def index(request):
    latest_provider_list = RegistrationInfo.objects.order_by('registration_date')

    context = {'latest_provider_list': latest_provider_list}

    return render(request, 'provider_registration/index.html', context)


def detail(request, provider_short_name):
    provider = get_object_or_404(RegistrationInfo, provider_short_name=provider_short_name)
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


def save_other_info(provider_short_name, base_url):
    try:
        RegistrationInfo.objects.get(provider_short_name=provider_short_name)
        logger.info('{} already exists'.format(provider_short_name))
        return render_to_response('provider_registration/already_exists.html', {'provider': provider_short_name})
    except ObjectDoesNotExist:
        logger.info('SAVING {}'.format(provider_short_name))
        RegistrationInfo(
            provider_short_name=provider_short_name,
            base_url=base_url,
            registration_date=timezone.now()
        ).save()


def save_oai_info(provider_short_name, base_url):
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

    all_sets = all_content.xpath('//oai_dc:set', namespaces=NAMESPACES)
    all_set_info = [one.getchildren() for one in all_sets]

    set_groups = []
    for item in all_set_info:
        print(len(item))
        one_group = (item[0].text, item[1].text)
        set_groups.append(one_group)

    # request 2 for records 30 days back just in case
    start_date = str(date.today() - timedelta(30))
    prop_url = base_url + '?verb=ListRecords&metadataPrefix=oai_dc&from={}T00:00:00Z'.format(start_date)
    prop_data_request = requests.get(prop_url)
    all_prop_content = etree.XML(prop_data_request.content)
    pre_names = all_prop_content.xpath('//ns0:metadata', namespaces=NAMESPACES)[0].getchildren()[0].getchildren()
    all_names = [name.tag.replace('{' + NAMESPACES['dc'] + '}', '') for name in pre_names]
    property_names = list({name for name in all_names if name not in BASE_SCHEMA})

    # check to see if provider with that name exists
    try:
        RegistrationInfo.objects.get(provider_short_name=provider_short_name)
        print('{} already exists'.format(provider_short_name))
        return render_to_response('provider_registration/already_exists.html', {'provider': provider_short_name})
    except ObjectDoesNotExist:
        print('SAVING {}'.format(provider_short_name))
        RegistrationInfo(
            provider_short_name=provider_short_name,
            base_url=base_url,
            property_list=property_names,
            approved_sets=set_groups,
            registration_date=timezone.now()
        ).save()


def register_provider(request):
    if request.method == 'POST':
        if not request.POST.get('property_list'):
            name = request.POST['provider_short_name']
            base_url = request.POST['base_url']

            if request.POST.get('oai_provider') == 'False':
                save_other_info(name, base_url)
                form = OtherProviderForm(
                    {
                        'provider_short_name': name,
                        'base_url': base_url,
                        'property_list': 'enter properties here'
                    }
                )
                return render(
                    request,
                    'provider_registration/other_registration_form.html',
                    {'form': form}
                )

            print("About to save {} in OAI format".format(name))
            save_oai_info(name, base_url)
            pre_saved_data = RegistrationInfo.objects.get(provider_short_name=name)

            approved_set_list = pre_saved_data.approved_sets.split(',')
            approved_set_list = [item.replace('[', '').replace(']', '') for item in approved_set_list]
            approved_set_set = set([(item, item) for item in approved_set_list])

            form = OAIProviderForm(
                {
                    'provider_short_name': name,
                    'base_url': base_url,
                    'property_list': pre_saved_data.property_list
                },
                choices=approved_set_set
            )

            return render(
                request,
                'provider_registration/oai_registration_form.html',
                {'form': form}
            )
        else:
            print('Now Updating data!')
            if request.POST.get('approved_sets', False):
                choices = set([(item, item) for item in request.POST['approved_sets']])
                form_data = OAIProviderForm(request.POST, choices=choices)

                object_to_update = RegistrationInfo.objects.get(provider_short_name=form_data['provider_short_name'].value())

                object_to_update.property_list = form_data['property_list'].value()
                object_to_update.approved_sets = str(form_data['approved_sets'].value())

                object_to_update.save()
            else:
                form_data = OtherProviderForm(request.POST)
                object_to_update = RegistrationInfo.objects.get(provider_short_name=form_data['provider_short_name'].value())
                object_to_update.property_list = form_data['property_list'].value()

                object_to_update.save()

            return render(
                request,
                'provider_registration/confirmation.html',
                {'provider': form_data['provider_short_name'].value()}
            )
