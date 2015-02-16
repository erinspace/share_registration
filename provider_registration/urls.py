from django.conf.urls import patterns, url

from provider_registration import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<provider_name>.*)/$', views.detail, name='detail'),
)
