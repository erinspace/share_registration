import logging

from lxml.etree import XMLSyntaxError

from django.utils import timezone
from django.forms.util import ErrorList
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.decorators.clickjacking import xframe_options_exempt

from provider_registration import utils

from provider_registration.models import RegistrationInfo
from provider_registration.forms import OAIProviderForm, OtherProviderForm, InitialProviderForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PLACEHOLDER_SHORTNAME = 'temp_shortname'


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


@xframe_options_exempt
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
        success = False
    except ObjectDoesNotExist:
        logger.info('SAVING {}'.format(provider_long_name))
        RegistrationInfo(
            provider_long_name=provider_long_name,
            base_url=base_url,
            registration_date=timezone.now(),
            provider_short_name=PLACEHOLDER_SHORTNAME
        ).save()
        success = True
    return success


def save_oai_info(provider_long_name, base_url):
    """ Gets and saves information about the OAI source
    """
    success = {'value': False, 'reason': 'Provider name already exists'}
    try:
        oai_properties = utils.get_oai_properties(base_url)

        # check to see if provider with that name exists
        try:
            RegistrationInfo.objects.get(provider_long_name=provider_long_name)

        except ObjectDoesNotExist:
            logger.info('SAVING {}'.format(provider_long_name))
            RegistrationInfo(
                provider_long_name=provider_long_name,
                base_url=base_url,
                property_list=oai_properties['properties'],
                approved_sets=oai_properties['sets'],
                registration_date=timezone.now(),
                provider_short_name=PLACEHOLDER_SHORTNAME
            ).save()
            success['value'] = True
            success['reason'] = '{} registered and saved successfully'.format(provider_long_name)

    except XMLSyntaxError:
        success['reason'] = 'XML Not Valid'

    logger.info(success['reason'])
    return success


def render_oai_provider_form(request, name, base_url):
    saving_successful = save_oai_info(name, base_url)
    if saving_successful['value']:
        pre_saved_data = RegistrationInfo.objects.get(provider_long_name=name)

        approved_set_set = utils.format_set_choices(pre_saved_data)

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
            {'form': form, 'name': name, 'base_url': base_url}
        )
    elif saving_successful['reason'] == 'XML Not Valid':
        form = InitialProviderForm(request.POST)
        form.is_valid()
        form._errors["base_url"] = ErrorList(["OAI-PMH XML not valid, please enter a valid OAI PMH url"])
        return render(
            request,
            'provider_registration/initial_registration_form.html',
            {'form': form}
        )
    else:
        return render_to_response('provider_registration/already_exists.html', {'provider': name})


def render_other_provider_form(request, name, base_url):
    saving_successful = save_other_info(name, base_url)
    if saving_successful:
        form = OtherProviderForm(
            {
                'provider_long_name': name,
                'base_url': base_url,
                'property_list': 'enter properties here'
            }
        )
        return render(
            request,
            'provider_registration/other_registration_form.html',
            {'form': form, 'name': name, 'base_url': base_url}
        )
    else:
        return render_to_response('provider_registration/already_exists.html', {'provider': name})


def update_oai_entry(request):
    choices = {(item, item) for item in request.POST['approved_sets']}
    form_data = OAIProviderForm(request.POST, choices=choices)

    object_to_update = RegistrationInfo.objects.get(provider_long_name=form_data['provider_long_name'].value())

    object_to_update.property_list = form_data['property_list'].value()
    object_to_update.approved_sets = str(form_data['approved_sets'].value())

    object_to_update.save()
    return form_data


def update_other_entry(request):
    form_data = OtherProviderForm(request.POST)
    object_to_update = RegistrationInfo.objects.get(provider_long_name=form_data['provider_long_name'].value())
    object_to_update.property_list = form_data['property_list'].value()

    object_to_update.save()
    return form_data


@xframe_options_exempt
def register_provider(request):
    """ Function to register a provider. This does all the work for
    registration, calling out to other functions for processing
    """
    if not request.POST.get('property_list'):
        # this is the initial post, and needs to be checked
        form = InitialProviderForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                'provider_registration/initial_registration_form.html',
                {'form': form}
            )
        name = request.POST['provider_long_name']
        base_url = request.POST['base_url']
        # if it's a first request and not an oai request, render the other provider form
        if not request.POST.get('oai_provider'):
            form = render_other_provider_form(request, name, base_url)
            return form
        else:
            # If it's made it this far, request is an OAI provider
            form = render_oai_provider_form(request, name, base_url)
            return form
    else:
        # Update the requested entries
        if request.POST.get('approved_sets', False):
            form_data = update_oai_entry(request)
        else:
            form_data = update_other_entry(request)

        return render(
            request,
            'provider_registration/confirmation.html',
            {'provider': form_data['provider_long_name'].value()}
        )
