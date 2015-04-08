from push_endpoint import views
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter, Route

urlpatterns = [
    url(r'^api/?', include([
        url(r'^$', views.DataList.as_view()),
        url(r'^established/?$', views.EstablishedDataList.as_view()),
        url(r'^(?P<pk>[0-9]+)/', views.DataDetail.as_view(), name='data-detail'),
        url(r'^get-api-key/?$', views.render_api_form, name='get-api-key'),
        url(r'^help/?$', views.render_api_help, name='help'),
        url(r'^api-auth/?$', include('rest_framework.urls', namespace='rest_framework')),
    ]))
]


class BulkUpdateRouter(DefaultRouter):
    routes = SimpleRouter.routes
    routes[0] = Route(
        url=r'^data/$',
        mapping={
            'get': 'list',
            'post': 'create',
            'put': 'bulk_update',
            'patch': 'partial_bulk_update'
        },
        name='pushed-data',
        initkwargs={'suffix': 'List'}
    )

router = BulkUpdateRouter()
# router.register(r'data/', views.DataList.as_view(), base_name='pushed-data')
# router.register(r'data/established', views.DataList.as_view(), base_name='pushed-data-established')


urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls
