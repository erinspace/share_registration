from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from push_endpoint import views

urlpatterns = [
    url(r'^pushed_data/$', views.DataList.as_view()),
    url(r'^pushed_data/(?P<pk>[0-9]+)/$', views.DataDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
