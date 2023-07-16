import datetime
from datetime import timedelta

from rest_framework import serializers

from attendance.constants import STATUS_OPEN
from attendance.models.attendance_detail_model import AttendanceDetail
from attendance.models.attendance_model import Attendance


class AttendanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceDetail
        fields = "__all__"

        extra_kwargs = {
            "branch": {"read_only": True},
            "attendance": {"read_only": True},
        }

    def check_right_attendance_date(self, check_in, employee):
        shift_start_datetime = datetime.datetime.combine(check_in.date(), employee.policy.working_policy_start_date)
        shift_end_datetime = shift_start_datetime + timedelta(hours=employee.policy.working_hours)
        if (
            shift_start_datetime - timedelta(hours=6)
            < check_in.replace(tzinfo=None)
            < shift_end_datetime + timedelta(hours=6)
        ):
            return check_in.date()
        else:
            return check_in.date() - timedelta(days=1)

    def create_attendance(self, date, employee, check_in):
        attendance = Attendance.objects.create(
            date=date,
            employee=employee,
            check_in=check_in,
            status=STATUS_OPEN,
            shift_start_time=employee.policy.working_policy_start_date,
            shift_end_time=employee.policy.working_policy_end_date,
        )
        return attendance

    def get_or_create_parent_attendance(self, check_in, employee):
        if not employee.branch:
            raise ValueError("this employee has no branch please set him a branch first")
        if not employee.policy:
            raise ValueError("this employee has no working policy please set him a one first")

        right_date = self.check_right_attendance_date(check_in, employee)
        attendance = Attendance.objects.filter(
            date=right_date,
            employee=employee,
        ).first()
        if attendance:
            return attendance
        else:
            return self.create_attendance(right_date, employee, check_in)

    def create(self, validated_data):
        employee = self.context.get("employee")
        attendance = self.get_or_create_parent_attendance(validated_data["check_in"], employee)
        if attendance.attendance_details:
            if attendance.attendance_details.filter(check_out=None).exists():
                raise serializers.ValidationError("There is transaction that has no check out please set it first")

            if attendance.attendance_details.filter(check_out__gte=validated_data["check_in"]).exists():
                raise serializers.ValidationError(
                    "There is transaction that has check out date after this check in date"
                )

        attendance_detail = AttendanceDetail.objects.create(
            attendance=attendance, **validated_data, branch=attendance.employee.branch
        )
        return attendance_detail

    def update(self, instance, validated_data):
        attendance = instance.attendance
        attendance_details = attendance.attendance_details.exclude(id=instance.id)
        if validated_data.get("check_in"):
            if attendance_details.filter(
                check_in__lte=validated_data.get("check_in"), check_out__gte=validated_data.get("check_in")
            ).exists():
                raise serializers.ValidationError("the date you entered is within another transaction ")
            instance.check_in = validated_data.get("check_in")
            if instance.check_in == attendance.check_in:
                attendance.check_in = validated_data.get("check_in")
            elif validated_data.get("check_in") < attendance.check_in:
                attendance.check_in = validated_data.get("check_in")

        if validated_data.get("check_out"):
            check_in = validated_data.get("check_in", getattr(self.instance, "check_in", None))
            if attendance_details.filter(
                check_in__lte=validated_data.get("check_out"), check_out__gte=validated_data.get("check_out")
            ).exists():
                raise serializers.ValidationError("the date you entered is within another transaction ")
            if attendance_details.filter(
                check_out__lte=validated_data.get("check_out"), check_in__gte=check_in
            ).exists():
                raise serializers.ValidationError("there is a complete transaction between this transaction dates  ")
            instance.check_out = validated_data.get("check_out")
            if attendance.check_out:
                if instance.check_out == attendance.check_out:
                    check_out = validated_data.get("check_out")
                    for detail in attendance_details:
                        if detail.check_out > check_out:
                            check_out = detail.check_out

                    attendance.check_out = check_out

        instance.save()
        attendance.status = STATUS_OPEN
        attendance.save()
        return instance

    def validate(self, data):
        check_in = data.get("check_in", getattr(self.instance, "check_in", None))
        check_out = data.get("check_out", getattr(self.instance, "check_out", None))
        if check_out and check_in and check_out < check_in:
            raise serializers.ValidationError("The check_out date must be after the check_in date.")

        if check_out and check_in and check_out > (check_in + timedelta(hours=24)):
            raise serializers.ValidationError("The check_out date cant be after 1 day of its check_in .")

        return data

    def validate_check_out(self, value):
        if not value:
            raise serializers.ValidationError("check out cannot be empty")

        return value
