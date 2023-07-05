from datetime import date

from rest_framework import serializers

from ..models.policie_model import Policie


class PolicieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policie
        fields = "__all__"

    # def create(self, validated_data):
    #     user = self.context.get('user')
    #     company =
    #     policie_obj = Policie(**validated_data)
    #     policie_obj.company= company
    #     policie_obj.created_by = user
    #     policie_obj.created_at = date.today(),
    #     policie_obj.save()
    #     return policie_obj

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
