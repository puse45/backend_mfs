import logging

from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from pointer.models import ClosestPointCompute
from pointer.serializers import ClosestPointComputeSerializer
from pointer.tasks import close_point_calculator

# Create your views here.

logger = logging.getLogger(__file__)


class ClosestPointsView(generics.GenericAPIView):
    queryset = ClosestPointCompute.objects.all()
    serializer_class = ClosestPointComputeSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("id",)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context=self.get_serializer_context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # task = close_point_calculator.delay(points=serializer.data.get("points"), id=serializer.data.get("id"))
            # logger.info("Task id to closest point %s", task.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if request.GET.get("id"):
                queryset = self.get_queryset().filter(pk=request.GET.get("id"))
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
