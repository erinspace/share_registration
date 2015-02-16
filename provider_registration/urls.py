from django.conf.urls import patterns, url

from provider_registration import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^provider_detail/(?P<provider_name>.*)/$', views.detail, name='detail'),
    url('self_register', views.register_provider, name='self_register'),
)
