from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response

from ..permissions import BaseAdminPermission, BlacklistPermission
from .mixins import (
    BaseCreateModelMixin,
    BaseRetrieveModelMixin,
    BaseListModelMixin,
    BaseUpdateModelMixin,
    BaseDestroyModelMixin,
)


@permission_classes((BlacklistPermission,))
class BaseViewSet(
    BaseCreateModelMixin,
    BaseRetrieveModelMixin,
    BaseListModelMixin,
    BaseUpdateModelMixin,
    BaseDestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Base API viewset for Base APIs.
    """

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        DjangoModelPermissions,
    ]

    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            # Occasionally client apps attempt querying for an item with invalid ids e.g. 'undefined'
            obj = get_object_or_404(queryset, **filter_kwargs)
            # May raise a permission denied
            self.check_object_permissions(self.request, obj)
            return obj
        except (ValueError, ValidationError) as e:
            return Http404

    def get_serializer_class(self):
        try:
            return self.action_serializers[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class BaseStandardViewSet(BaseViewSet):
    """
    Read-only viewset that provides `retrieve`, `create`, and `list` actions.
    """

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@permission_classes((BlacklistPermission,))
class BaseWriteOnlyViewSet(BaseCreateModelMixin, viewsets.GenericViewSet):
    """
    Write-only viewset that provides `create` action.
    """

    def get_serializer_class(self):
        try:
            return self.action_serializers[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


@permission_classes((BlacklistPermission,))
class BaseImmutableViewSet(
    BaseCreateModelMixin,
    BaseRetrieveModelMixin,
    BaseListModelMixin,
    BaseUpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset that prevents `delete` action.
    """

    def get_serializer_class(self):
        try:
            return self.action_serializers[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


@permission_classes((BlacklistPermission,))
class BaseReadOnlyViewSet(
    BaseRetrieveModelMixin, BaseListModelMixin, viewsets.GenericViewSet
):
    """
    Read-only viewset that provides `retrieve`, `create`, and `list` actions.
    """

    def get_serializer_class(self):
        try:
            return self.action_serializers[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes((BaseAdminPermission,))
class BaseAdminOnlyViewSet(BaseViewSet):
    """
    Admin Only viewset that provides `retrieve`, `create`, `list`, and `destroy` actions.
    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
