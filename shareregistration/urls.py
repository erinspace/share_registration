from django.contrib import admin
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^provider_registration/', include('provider_registration.urls', namespace="provider_registration")),
    url(r'^admin/', include(admin.site.urls)),
)
