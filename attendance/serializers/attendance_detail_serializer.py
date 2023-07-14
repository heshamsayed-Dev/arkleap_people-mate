import datetime
from datetime import timedelta

from rest_framework import serializers

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

    def get_or_create_parent_attendance(self, check_in, employee):
        try:
            if not employee.branch:
                raise ValueError("this employee has no branch please set him a branch first")
            if not employee.policy:
                raise ValueError("this employee has no working policy please set him a one first")

            attendances = Attendance.objects.filter(
                date__range=[check_in.date() - datetime.timedelta(days=1), check_in.date()],
                employee=employee,
                status="open",
            )

            if not attendances:
                raise Attendance.DoesNotExist()
            if attendances.count() == 2:
                attendance = attendances.get(date=check_in.date())

            else:
                if attendances[0].date == check_in.date():
                    attendance = attendances[0]

                else:
                    shift_start_datetime = datetime.datetime.combine(
                        attendances[0].date, attendances[0].shift_start_time
                    )

                    # case that shift from night to next day morning
                    if attendances[0].shift_start_time > attendances[0].shift_end_time:
                        shift_end_datetime = datetime.datetime.combine(
                            attendances[0].date + timedelta(days=1),
                            attendances[0].shift_end_time,
                        )
                    else:
                        shift_end_datetime = (
                            attendances[0].date + timedelta(days=1),
                            attendances[0].shift_end_time,
                        )

                    if (
                        shift_start_datetime
                        <= check_in.replace(tzinfo=None)
                        <= shift_end_datetime + timedelta(hours=5)
                    ):
                        attendance = attendances[0]
                    else:
                        raise Attendance.DoesNotExist()

        except Attendance.DoesNotExist:
            attendance = Attendance.objects.create(
                date=check_in.date(),
                employee=employee,
                check_in=check_in,
                status="open",
                shift_start_time=employee.policy.working_policy_start_date,
                shift_end_time=employee.policy.working_policy_end_date,
                creation_method="automatic",
            )
        return attendance

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

    def validate(self, data):
        check_in = data.get("check_in", getattr(self.instance, "check_in", None))
        check_out = data.get("check_out", getattr(self.instance, "check_out", None))
        if check_out and check_in and check_out < check_in:
            raise serializers.ValidationError("The check_out date must be after the check_in date.")

        if check_out and check_in and check_out > (check_in + timedelta(hours=24)):
            raise serializers.ValidationError("The check_out date cant be after 1 day of its check_in .")

        att = Attendance.objects.filter(date=check_in.date(), status="closed").first()
        if att:
            raise serializers.ValidationError(
                "you cant create or edit any transaction for this date it's attendance is already closed ."
            )

        return data

    def validate_check_out(self, value):
        if not value:
            raise serializers.ValidationError("check out cannot be empty")

        return value
