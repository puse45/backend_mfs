from rest_framework import serializers

from pointer.models import ClosestPointCompute


class ClosestPointComputeSerializer(serializers.ModelSerializer):
    # points = serializers.ListSerializer(required=True)

    class Meta:
        model = ClosestPointCompute
        fields = (
            "id",
            "points",
            "computation_result",
            "is_processing",
            "is_done",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["computation_result", "is_processing", "is_done"]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate(self, attrs):
        return attrs
