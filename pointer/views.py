from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from pointer.serializers import ClosestPointComputeSerializer


# Create your views here.
class ClosestPointsView(generics.GenericAPIView):
    serializer_class = ClosestPointComputeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context=self.get_serializer_context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
