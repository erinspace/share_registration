from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from provider_registration import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^provider_detail/(?P<provider_long_name>.*)/$', views.detail, name='detail'),
    url(r'^register', views.register_provider, name='register'),
    url(r'^pre_register', views.get_provider_info, name='pre_register'),
    url(r'^contact_information', views.get_contact_info, name='contact_information'),
    url(r'^metadata_information', views.get_metadata_info, name='metadata_information'),

)

urlpatterns += staticfiles_urlpatterns()
