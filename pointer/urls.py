from django.urls import include, path
from rest_framework.routers import DefaultRouter

from pointer.views import ClosestPointsView

app_name = "pointer"

# Register routes
router = DefaultRouter()

api_urlpatterns = [
    path(
        "",
        ClosestPointsView.as_view(),
    ),
]
urlpatterns = []
