from datetime import date

from rest_framework import serializers

from ..models.policy_model import Policy


class policySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = "__all__"

    def update(self, instance, validated_data, *args, **kwargs):
        try:
            user = self.context.get("user")
            instance.last_update_date = date.today()
            instance.last_update_by = user
            instance.working_hours = validated_data.get("working_hours", instance.working_hours)
            instance.start_of_working_hours = validated_data.get(
                "start_of_working_hours", instance.start_of_working_hours
            )
            instance.end_of_working_hours = validated_data.get("end_of_working_hours", instance.end_of_working_hours)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError(detail={f"error:{e}, please connect to admin"})
