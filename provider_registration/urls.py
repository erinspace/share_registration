from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from provider_registration import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^provider_detail/(?P<provider_short_name>.*)/$', views.detail, name='detail'),
    url(r'^register', views.register_provider, name='register'),
    url(r'^pre_register', views.get_provider_info, name='pre_register'),
)

urlpatterns += staticfiles_urlpatterns()
