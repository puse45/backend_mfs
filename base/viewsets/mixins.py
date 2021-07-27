import csv
import logging

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

logger = logging.getLogger(__name__)


class BaseCreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        app = self.get_serializer_class().Meta.model._meta.app_label
        model = self.get_serializer_class().Meta.model.__name__
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if serializer.is_valid():
            self.perform_create(serializer)
            data = serializer.data
            # Log activity or notify subscribers.
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(data),
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class BaseRetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BaseListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        no_pagination = self.request.query_params.get("all", False)
        if no_pagination:
            self.pagination_class = None
        queryset = self.filter_queryset(self.get_queryset())
        if not no_pagination:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BaseUpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        print("Partial ", serializer)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class BaseDestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # Archive data
        # instance.delete()
        instance.is_archived = True
        instance.save()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected"
