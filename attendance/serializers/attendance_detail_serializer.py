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

    # validates if check in of transaction is between other transaction check in and check out
    def validate_overlapping_in_check_in(self, check_in, attendance_details):
        if attendance_details.filter(check_in__lte=check_in, check_out__gte=check_in).exists():
            raise serializers.ValidationError("the check in date time you entered is within another transaction ")

    # validates if check out of transaction is between other transaction check in and check out
    def validate_overlapping_in_check_out(self, check_out, attendance_details):
        if attendance_details.filter(check_in__lte=check_out, check_out__gte=check_out).exists():
            raise serializers.ValidationError("the check out date time you entered is within another transaction ")

    # validates if check in and check out of this transaction contains a whole transaction between them
    def validate_transaction_overlapping(self, check_in, check_out, attendance_details):
        if attendance_details.filter(check_out__lte=check_out, check_in__gte=check_in).exists():
            raise serializers.ValidationError("there is a complete transaction between this transaction dates  ")

    # returns right attendance date for transaction being created
    def get_right_attendance_date(self, check_in, employee):
        shift_start_datetime = datetime.datetime.combine(check_in.date(), employee.policy.working_policy_start_date)
        shift_end_datetime = shift_start_datetime + timedelta(hours=employee.policy.working_hours)

        # checks if shift starts and ends in the same day then the transaction is related to this date
        if shift_start_datetime.date() == shift_end_datetime.date():
            return check_in.date()

        # checks if  transaction check_in is between (shift start datetime - buffer)
        #  and (shift end datetime + buffer)
        if (
            shift_start_datetime - timedelta(hours=6)
            < check_in.replace(tzinfo=None)
            < shift_end_datetime + timedelta(hours=6)
        ):
            return check_in.date()

        # if it passed the above conditions then this transaction is related to the day before
        # check_in date
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

        right_date = self.get_right_attendance_date(check_in, employee)
        attendance = Attendance.objects.filter(
            date=right_date,
            employee=employee,
        ).first()
        # checks whether there is a created attendance for this transaction or create a new one
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
                self.validate_overlapping_in_check_in(validated_data["check_in"], attendance.attendance_details)
                attendance.check_in = validated_data["check_in"]

            if validated_data.get("check_out"):
                self.validate_overlapping_in_check_out(validated_data.get("check_out"), attendance.attendance_details)
                self.validate_transaction_overlapping(
                    validated_data["check_in"], validated_data["check_out"], attendance.attendance_details
                )

        # if any transaction created for attendance entity then it's status should be open
        attendance_detail = AttendanceDetail.objects.create(
            attendance=attendance, **validated_data, branch=attendance.employee.branch
        )
        attendance.status = STATUS_OPEN
        attendance.save()
        return attendance_detail

    def update(self, instance, validated_data):
        attendance = instance.attendance
        attendance_details = attendance.attendance_details.exclude(id=instance.id)
        if validated_data.get("check_in"):
            self.validate_overlapping_in_check_in(validated_data.get("check_in"), attendance_details)
            instance.check_in = validated_data.get("check_in")
            # checks if this transaction is the first transaction made for this parent attendance
            if instance.check_in == attendance.check_in:
                attendance.check_in = validated_data.get("check_in")
            # checks if this transaction check in is less than the attendance check in time
            elif validated_data.get("check_in") < attendance.check_in:
                attendance.check_in = validated_data.get("check_in")

        if validated_data.get("check_out"):
            check_in = validated_data.get("check_in", getattr(self.instance, "check_in", None))
            self.validate_overlapping_in_check_out(validated_data.get("check_out"), attendance_details)
            self.validate_transaction_overlapping(check_in, validated_data.get("check_out"), attendance_details)
            # deletes attendance check out value if existed because it will be calculated again
            if attendance.check_out:
                attendance.check_out = None
            instance.check_out = validated_data.get("check_out")

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
