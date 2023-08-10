from rest_framework import serializers

from .attendance_serializer import AttendanceSerializer


class DashboardSerializer(serializers.Serializer):
    num_employees = serializers.IntegerField()
    num_branches = serializers.IntegerField()
    num_permissions = serializers.IntegerField()
    num_attendances = serializers.IntegerField()
    attendances = AttendanceSerializer(many=True)
