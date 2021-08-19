from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from pointer.models import ClosestPointCompute
from pointer.tasks import processor


class ClosestPointComputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosestPointCompute
        fields = (
            "id",
            "points",
            "result",
            "is_processing",
            "is_done",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["result", "is_processing", "is_done"]

    def create(self, validated_data):
        """On save points are submitted to be processed via processor method"""
        p1, p2, mi = processor(points=validated_data.get("points"))

        payload = {
            "closest points": {"point A": p1, "point B": p2},
            "distance between": mi,
        }
        validated_data["result"] = payload
        validated_data["is_processing"] = False
        validated_data["is_done"] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
