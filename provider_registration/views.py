import logging

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, render_to_response

from provider_registration.utils import get_oai_properties

from provider_registration.models import RegistrationInfo
from provider_registration.forms import OAIProviderForm, OtherProviderForm, InitialProviderForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NAMESPACES = {'dc': 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/',
              'ns0': 'http://www.openarchives.org/OAI/2.0/'}
BASE_SCHEMA = ['title', 'contributor', 'creator', 'subject', 'description']


def index(request):
    latest_provider_list = RegistrationInfo.objects.order_by('registration_date')

    context = {'latest_provider_list': latest_provider_list}

    return render(request, 'provider_registration/index.html', context)


def detail(request, provider_long_name):
    provider = get_object_or_404(RegistrationInfo, provider_long_name=provider_long_name)
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


def save_other_info(provider_long_name, base_url):
    try:
        RegistrationInfo.objects.get(provider_long_name=provider_long_name)
        logger.info('{} already exists'.format(provider_long_name))
        return render_to_response('provider_registration/already_exists.html', {'provider': provider_long_name})
    except ObjectDoesNotExist:
        logger.info('SAVING {}'.format(provider_long_name))
        RegistrationInfo(
            provider_long_name=provider_long_name,
            base_url=base_url,
            registration_date=timezone.now()
        ).save()


def save_oai_info(provider_long_name, base_url):
    """ Makes 2 requests to the provided base URL:
        1 for the sets available
        1 for the list of properties
        The sets available are added as multiple selections for the next form,
        the properties are pre-loaded into the properties field.
    """

    oai_properties = get_oai_properties(base_url)

    # check to see if provider with that name exists
    try:
        RegistrationInfo.objects.get(provider_long_name=provider_long_name)
        logger.info('{} already exists'.format(provider_long_name))
        return render_to_response('provider_registration/already_exists.html', {'provider': provider_long_name})
    except ObjectDoesNotExist:
        logger.info('SAVING {}'.format(provider_long_name))
        RegistrationInfo(
            provider_long_name=provider_long_name,
            base_url=base_url,
            property_list=oai_properties['properties'],
            approved_sets=oai_properties['sets'],
            registration_date=timezone.now()
        ).save()


def register_provider(request):
    """ Function to register a provider. This does all the work for
    registration, calling out to other functions for processing
    """
    if request.method == 'POST':
        # If there's no prop list, it's a first request or non-oai request
        if not request.POST.get('property_list'):
            name = request.POST['provider_long_name']
            base_url = request.POST['base_url']
            # if it's a first request and not an oai request, render the other provider form
            if not request.POST.get('oai_provider'):
                save_other_info(name, base_url)
                form = OtherProviderForm(
                    {
                        'provider_long_name': name,
                        'base_url': base_url,
                        'property_list': 'enter properties here'
                    }
                )
                if form.is_valid():
                    return render(
                        request,
                        'provider_registration/other_registration_form.html',
                        {'form': form}
                    )
                else:
                    print('NOT VALID.')
                    form = InitialProviderForm()
                    return render(
                        request,
                        'provider_registration/initial_registration_form.html',
                        {'form': form}
                    )
            else:
                # If it's made it this far, request is an OAI provider
                logger.info("About to save {} in OAI format".format(name))
                save_oai_info(name, base_url)
                pre_saved_data = RegistrationInfo.objects.get(provider_long_name=name)

                approved_set_list = pre_saved_data.approved_sets.split(',')
                approved_set_list = [item.replace('[', '').replace(']', '') for item in approved_set_list]
                approved_set_set = set([(item, item) for item in approved_set_list])
                # render an OAI form with the request data filled in
                form = OAIProviderForm(
                    {
                        'provider_long_name': name,
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
            # If there's no approved sets yet, render the pre-OAI provider form
            if request.POST.get('approved_sets', False):
                choices = {(item, item) for item in request.POST['approved_sets']}
                form_data = OAIProviderForm(request.POST, choices=choices)

                object_to_update = RegistrationInfo.objects.get(provider_long_name=form_data['provider_long_name'].value())

                object_to_update.property_list = form_data['property_list'].value()
                object_to_update.approved_sets = str(form_data['approved_sets'].value())

                object_to_update.save()
            else:
                form_data = OtherProviderForm(request.POST)
                object_to_update = RegistrationInfo.objects.get(provider_long_name=form_data['provider_long_name'].value())
                object_to_update.property_list = form_data['property_list'].value()

                object_to_update.save()

            return render(
                request,
                'provider_registration/confirmation.html',
                {'provider': form_data['provider_long_name'].value()}
            )
