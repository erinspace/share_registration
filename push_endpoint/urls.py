from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from push_endpoint import views

from rest_framework_bulk.routes import BulkRouter

urlpatterns = [
    # url(r'^pushed_data/$', views.DataList.as_view()),
    url(r'^pushed_data/(?P<pk>[0-9]+)/$', views.DataDetail.as_view(), name='data-detail'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail')
]

router = BulkRouter()
router.register(r'pushed_data/', views.DataList)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls
