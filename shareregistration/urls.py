from django.contrib import admin
from django.conf.urls import patterns, include, url

# from shareregistration import views
from push_endpoint import views as push_views

urlpatterns = patterns(
    '',
    url(r'^$', push_views.DataList.as_view(), name='index'),
    url(r'^', include('push_endpoint.urls')),
    url(r'^share-admin', include(admin.site.urls)),
    url(r'^provider_registration', include('provider_registration.urls', namespace="provider_registration")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
