import logging

from lxml.etree import XMLSyntaxError

from django.utils import timezone
from django.forms.util import ErrorList
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.decorators.clickjacking import xframe_options_exempt

from provider_registration import utils

from provider_registration.models import RegistrationInfo
from provider_registration.forms import OAIProviderForm, OtherProviderForm, InitialProviderForm, ContactInfoForm, MetadataQuestionsForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PLACEHOLDER = 'temp_value'


@xframe_options_exempt
def index(request):
    latest_provider_list = RegistrationInfo.objects.order_by('-registration_date')[:20]

    context = {'latest_provider_list': latest_provider_list}

    return render(request, 'provider_registration/index.html', context)


@xframe_options_exempt
def detail(request, provider_long_name):
    provider = get_object_or_404(RegistrationInfo, provider_long_name=provider_long_name)
    return render(
        request,
        'provider_registration/detail.html',
        {'provider': provider}
    )


@xframe_options_exempt
def get_contact_info(request):
    """ Shows initial provider form
    """
    if request.method == 'GET':
        form = ContactInfoForm()
        return render(
            request,
            'provider_registration/contact_information.html',
            {'form': form}
        )
    else:
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            reg_id = save_contact_info(contact_name, contact_email)
            form = MetadataQuestionsForm({'reg_id': reg_id, 'meta_license': ' '})
            return render(
                request,
                'provider_registration/metadata_questions.html',
                {'form': form}
            )
        else:
            return render(
                request,
                'provider_registration/contact_information.html',
                {'form': form}
            )


def save_contact_info(contact_name, contact_email):
    logger.info('Saving provider with contact name {} and email {}'.format(contact_name, contact_email))
    RegistrationInfo(
        contact_name=contact_name,
        contact_email=contact_email,
        provider_long_name=PLACEHOLDER,
        base_url=PLACEHOLDER,
        registration_date=timezone.now(),
        provider_short_name=PLACEHOLDER
    ).save()
    new_registration = RegistrationInfo.objects.last()
    return new_registration.id


@xframe_options_exempt
def save_metadata_render_provider(request):
    """
    Saves metadata info
    Shows basic provider questions form
    """
    form = MetadataQuestionsForm(request.POST)
    if form.is_valid() and request.POST['meta_license'] != ' ':
        reg_id = request.POST.get('reg_id')
        current_registration = RegistrationInfo.objects.get(id=reg_id)

        current_registration.meta_liscense = request.POST.get('meta_license')

        if request.POST.get('meta_tos'):
            current_registration.meta_tos = True
        if request.POST.get('meta_privacy'):
            current_registration.meta_privacy = True
        if request.POST.get('meta_sharing_tos'):
            current_registration.meta_sharing_tos = True
        if request.POST.get('meta_license_extended'):
            current_registration.meta_license_extended = True
        if request.POST.get('meta_future_license'):
            current_registration.meta_future_license = True

        current_registration.save()

        # TODO fix the example url that gets checked here?
        form = InitialProviderForm({
            'reg_id': reg_id,
            'provider_long_name': ' ',
            'base_url': 'http://example.com',
            'description': ' '
        })
        return render(
            request,
            'provider_registration/provider_questions.html',
            {'form': form}
        )

    else:
        form._errors["meta_license"] = ErrorList(['Please enter a license. If None, please enter "None."'])
        return render(
            request,
            'provider_registration/metadata_questions.html',
            {'form': form}
        )


def save_other_info(provider_long_name, base_url, reg_id):
    object_to_update = RegistrationInfo.objects.get(id=reg_id)

    object_to_update.provider_long_name = provider_long_name
    object_to_update.base_url = base_url
    object_to_update.registration_date = timezone.now()
    object_to_update.provider_short_name = PLACEHOLDER
    object_to_update.save()

    return True


def save_oai_info(provider_long_name, base_url, reg_id):
    """ Gets and saves information about the OAI source
    """
    success = {'value': False, 'reason': 'XML Not Valid'}
    try:
        oai_properties = utils.get_oai_properties(base_url)

        object_to_update = RegistrationInfo.objects.get(id=reg_id)

        object_to_update.provider_long_name = provider_long_name
        object_to_update.base_url = base_url
        object_to_update.property_list = oai_properties['properties']
        object_to_update.approved_sets = oai_properties['sets']
        object_to_update.registration_date = timezone.now()
        object_to_update.provider_short_name = PLACEHOLDER
        object_to_update.save()

        success['value'] = True
        success['reason'] = '{} registered and saved successfully'.format(provider_long_name)

    except XMLSyntaxError:
        success['reason'] = 'XML Not Valid'

    logger.info(success['reason'])
    return success


@xframe_options_exempt
def render_oai_provider_form(request, name, base_url, reg_id):
    saving_successful = save_oai_info(name, base_url, reg_id)
    if saving_successful['value']:
        pre_saved_data = RegistrationInfo.objects.get(id=reg_id)

        approved_set_set = utils.format_set_choices(pre_saved_data)

        # render an OAI form with the request data filled in
        form = OAIProviderForm(
            {
                'provider_long_name': name,
                'base_url': base_url,
                'property_list': pre_saved_data.property_list,
                'reg_id': reg_id
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
            'provider_registration/provider_questions.html',
            {'form': form}
        )
    else:
        return render_to_response('provider_registration/already_exists.html', {'provider': name})


@xframe_options_exempt
def render_other_provider_form(request, name, base_url, reg_id):
    saving_successful = save_other_info(name, base_url, reg_id)
    if saving_successful:
        form = OtherProviderForm(
            {
                'provider_long_name': name,
                'base_url': base_url,
                'property_list': 'enter properties here',
                'reg_id': reg_id
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
    object_to_update = RegistrationInfo.objects.get(id=request.POST['reg_id'])

    object_to_update.property_list = form_data['property_list'].value()
    object_to_update.approved_sets = str(form_data['approved_sets'].value())

    object_to_update.save()
    return form_data


def update_other_entry(request):
    form_data = OtherProviderForm(request.POST)
    object_to_update = RegistrationInfo.objects.get(id=request.POST['reg_id'])
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
                'provider_registration/provider_questions.html',
                {'form': form}
            )
        name = request.POST['provider_long_name']
        base_url = request.POST['base_url']
        reg_id = request.POST['reg_id']
        # if it's a first request and not an oai request, render the other provider form
        if not request.POST.get('oai_provider'):
            form = render_other_provider_form(request, name, base_url, reg_id)
            return form
        else:
            # If it's made it this far, request is an OAI provider
            form = render_oai_provider_form(request, name, base_url, reg_id)
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
