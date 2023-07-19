from datetime import timedelta

from rest_framework import serializers

from attendance.models.attendance_model import Attendance
from employee.models.employee_model import Employee


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

        extra_kwargs = {
            "check_out": {"required": True},
            "status": {"read_only": True},
            "creation_method": {"read_only": True},
        }

    def create(self, validated_data):
        attendance = Attendance.objects.create(
            **validated_data,
            shift_start_time=validated_data["employee"].policy.working_policy_start_date,
            shift_end_time=validated_data["employee"].policy.working_policy_end_date,
            worked_hours=(validated_data["check_out"] - validated_data["check_in"]).total_seconds() / 3600,
            status="closed",
            creation_method="manual",
        )
        return attendance

    def update(self, instance, validated_data):
        check_in = validated_data.get("check_in", getattr(self.instance, "check_in", None))
        check_out = validated_data.get("check_out", getattr(self.instance, "check_out", None))
        # here will check for date if changed will seek for new shift start time and end time
        # when added inside working policy
        if validated_data["check_in"] or validated_data["check_out"] and instance.creation_method == "automatic":
            raise serializers.ValidationError("you cant edit in this attendance it is created automatically")
        if validated_data["check_in"] or validated_data["check_out"] and instance.creation_method == "manual":
            instance.worked_hours = check_out - check_in
        if validated_data["employee"] and validated_data["employee"] != instance.employee.id:
            employee = Employee.objects.get(id=validated_data["employee"])
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
            att = Attendance.objects.filter(date=date, employee=employee).first()
            if att:
                raise serializers.ValidationError(" attendance with the same date has been created before")

        elif self.context["request"].method in ["PATCH", "PUT"]:
            att = Attendance.objects.filter(date=date, employee=employee).first()
            if att:
                if att.id != self.context["id"]:
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
