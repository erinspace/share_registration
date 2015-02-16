
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render

from provider_registration.forms import ProviderForm
from provider_registration.models import RegistrationInfo


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
        form = ProviderForm()
        return render(
            request,
            'provider_registration/self_registration_form.html',
            {'form': form})
