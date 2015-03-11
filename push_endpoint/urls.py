from django.conf.urls import url
from push_endpoint import views

urlpatterns = [
    url(r'^pushed_data/$', views.data_list),
    url(r'^pushed_data/(?P<pk>[0-9]+)/$', views.data_detail),
]
