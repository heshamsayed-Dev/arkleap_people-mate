from rest_framework import serializers

from employee.models.location_model import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

    def validate_latitude(self, value):
        if value < -90.0 or value > 90.0:
            raise serializers.ValidationError("Latitude must be between -90.0 and 90.0")
        return value

    def validate_longitude(self, value):
        if value < -180.0 or value > 180.0:
            raise serializers.ValidationError("Longitude must be between -180.0 and 180.0")
        return value
