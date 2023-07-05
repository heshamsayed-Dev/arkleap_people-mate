from rest_framework import serializers

from attendance.models.attendance_model import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
