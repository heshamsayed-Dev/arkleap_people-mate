from datetime import date

from rest_framework import serializers

from employee.models.employee_model import Employee

from ..models.policy_model import Policy


def get_company(user):
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        raise serializers.ValidationError(detail={"this user have no employee, please connect to admin"})
    except Employee.MultipleObjectsReturned:
        employee = Employee.objects.filter(user=user).last()
    return employee.company


class policySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        exclude = ("company", "created_by", "created_at", "last_update_by", "last_update_date")

    def create(self, validated_data):
        user = self.context.get("user")
        company = get_company(user)
        company = company
        policy_obj = Policy(**validated_data)
        policy_obj.company = company
        policy_obj.created_by = user
        policy_obj.created_at = (date.today(),)
        policy_obj.save()
        return policy_obj

    def update(self, instance, validated_data, *args, **kwargs):
        try:
            user = self.context.get("user")
            company = get_company(user)
            company = company
            instance.last_update_date = date.today()
            instance.last_update_by = user
            instance.working_hours = validated_data.get("working_hours", instance.working_hours)
            instance.working_policy_start_date = validated_data.get(
                "working_policy_start_date", instance.working_policy_start_date
            )
            instance.working_policy_end_date = validated_data.get(
                "working_policy_end_date", instance.working_policy_end_date
            )
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(detail={f"error:{e}, please connect to admin"})
