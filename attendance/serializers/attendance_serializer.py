from datetime import timedelta

from rest_framework import serializers

from attendance.constants import STATUS_CLOSED
from attendance.models.attendance_model import Attendance
from employee.models.employee_model import Employee


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

        extra_kwargs = {
            "check_out": {"required": True},
            "status": {"read_only": True},
        }

    def create(self, validated_data):
        attendance = Attendance.objects.create(
            **validated_data,
            shift_start_time=validated_data["employee"].policy.working_policy_start_date,
            shift_end_time=validated_data["employee"].policy.working_policy_end_date,
            worked_hours=(validated_data["check_out"] - validated_data["check_in"]).total_seconds() / 3600,
            status=STATUS_CLOSED,
        )
        return attendance

    def update(self, instance, validated_data):
        check_in = validated_data.get("check_in", getattr(self.instance, "check_in", None))
        check_out = validated_data.get("check_out", getattr(self.instance, "check_out", None))
        # here will check for date if changed will seek for new shift start time and end time
        # when added inside working policy
        if validated_data.get("check_in") or validated_data.get("check_out"):
            instance.worked_hours = (check_out - check_in).total_seconds() / 3600
        if validated_data.get("employee") and validated_data["employee"] != instance.employee.id:
            employee = Employee.objects.get(id=validated_data["employee"].id)
            instance.shift_start_time = employee.policy.working_policy_start_date
            instance.shift_end_time = employee.policy.working_policy_end_date
        instance.save()
        return instance

    def validate(self, data):
        check_in = data.get("check_in", getattr(self.instance, "check_in", None))
        check_out = data.get("check_out", getattr(self.instance, "check_out", None))
        date = data.get("date", getattr(self.instance, "date", None))
        employee = data.get("employee", getattr(self.instance, "employee", None))
        if not employee.policy:
            raise serializers.ValidationError(" cant create attendance for employee that has no working policy policy")

        if self.context["request"].method == "POST":
            attendance = Attendance.objects.filter(date=date, employee=employee).first()
            if attendance:
                raise serializers.ValidationError(" attendance with the same date has been created before")

        elif self.context["request"].method in ["PATCH", "PUT"]:
            attendance = Attendance.objects.filter(date=date, employee=employee).first()
            if attendance:
                if attendance.id != self.context["id"]:
                    raise serializers.ValidationError(
                        " another  attendance with the same date has been created before"
                    )

        if date != check_in.date():
            raise serializers.ValidationError(" attendance date cant be different from check in date")

        if check_out and check_in and check_out <= check_in:
            raise serializers.ValidationError("The check_out date must be after the check_in date.")

        if check_out and check_in and check_out > (check_in + timedelta(hours=24)):
            raise serializers.ValidationError("The check_out date cant be after 1 day of its check_in .")

        return data

    def validate_check_out(self, value):
        if not value:
            raise serializers.ValidationError("check out cannot be empty")

        return value
