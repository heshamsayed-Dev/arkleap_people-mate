from rest_framework import serializers


class AttendanceFilterSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, data):
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        if date_from and date_to:
            if date_to < date_from:
                raise serializers.ValidationError("date to cannot be before date from ")

        return data
