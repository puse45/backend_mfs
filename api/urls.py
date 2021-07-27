from django.urls import include, path
from rest_framework.routers import DefaultRouter

from pointer.urls import api_urlpatterns as pointer_urls

router = DefaultRouter()
app_name = "api"


urlpatterns = [
    path("", include(router.urls)),
    path("points/", include(pointer_urls)),
]
