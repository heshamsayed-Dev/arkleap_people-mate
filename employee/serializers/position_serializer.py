from rest_framework import serializers

from employee.models.position_model import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"
