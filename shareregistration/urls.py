from django.contrib import admin
from django.conf.urls import patterns, include, url

from shareregistration import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^', include('push_endpoint.urls')),
    url(r'^share-admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^provider_registration/', include('provider_registration.urls', namespace="provider_registration"))
)
