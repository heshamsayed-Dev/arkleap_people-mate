from rest_framework import serializers

from attendance.models.attendance_detail_model import AttendanceDetail


class AttendanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceDetail
        fields = "__all__"

    #   extra_kwargs={
    #         'attendance' : {'write_only':True},
    #     }
