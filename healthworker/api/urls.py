from .views import HealthWorkerRUDView, HealthWorkerAPIView
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^$', HealthWorkerAPIView.as_view(),name='post-listcreate'),
	url(r'^api-token-auth/',obtain_jwt_token, name='api-login'),
    url(r'^(?P<pk>\d+)/$', HealthWorkerRUDView.as_view(),name='post-rud'), #post-create
]
