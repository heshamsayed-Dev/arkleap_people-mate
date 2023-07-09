from datetime import date

from rest_framework import serializers

from employee.models.company_model import Company

from ..models.policy_model import Policy


class policySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        exclude = ("company", "created_by", "created_at", "last_update_by", "last_update_date")

    def create(self, validated_data):
        user = self.context.get("user")
        company = Company.objects.get(id=1)

        policy_obj = Policy(**validated_data)
        policy_obj.company = company
        policy_obj.created_by = user
        policy_obj.created_at = (date.today(),)
        policy_obj.save()
        return policy_obj

    def update(self, instance, validated_data, *args, **kwargs):
        try:
            user = self.context.get("user")
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
