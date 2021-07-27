from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "base"

router = DefaultRouter()
# Register routes

api_urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns = []
