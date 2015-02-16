from django.shortcuts import get_object_or_404, render

from provider_registration.models import RegistrationInfo


def index(request):
    latest_provider_list = RegistrationInfo.objects.order_by('registration_date')[:5]

    context = {'latest_provider_list': latest_provider_list}

    return render(request, 'provider_registration/index.html', context)


def detail(request, provider_name):
    provider = get_object_or_404(RegistrationInfo, provider_name=provider_name)
    return render(request, 'provider_registration/detail.html', {'provider': provider})
