from rest_framework import serializers

from attendance.models.attendance_model import Attendance
from datetime import timedelta

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

        extra_kwargs={
            'check_out' : {'required':True},
            'worked_hours':{'required':True},
            'status':{'required':True},
        }

    # def create(self, validated_data):
        # attendance=Attendance.objects.create(
        #         **validated_data,
        #         shift_start_time=validated_data['employee'].policy.shift_start,
        #         shift_end_time=validated_data['employee'].policy.shift_end
        #         worked_hours=(check_out - check_in).total_seconds()/3600
        #     )
        # return attendance    

    def validate(self, data):
        check_in = data.get('check_in', getattr(self.instance, 'check_in', None))
        check_out = data.get('check_out',getattr(self.instance, 'check_out', None))
        worked_hours = data.get('worked_hours',getattr(self.instance, 'worked_hours', None))
        date= data.get('date',getattr(self.instance, 'date', None))
        employee= data.get('employee',getattr(self.instance, 'employee', None))

        if self.context['request'].method == 'POST' :
            att= Attendance.objects.filter(date=date,employee=employee).first()
            if att :
                raise serializers.ValidationError(" attendance with the same date has been created before")

        elif self.context['request'].method in ['PATCH', 'PUT'] :
            att= Attendance.objects.filter(date=date,employee=employee).first()
            if att.id != self.context['id'] :
                raise serializers.ValidationError(" another  attendance with the same date has been created before")        


        if data.get('status'):
            if data.get('status') == 'open':
                raise serializers.ValidationError("if you create the attendance manually you must set the status to be closed")

        if date != check_in.date():
                raise serializers.ValidationError(" attendance date cant be different from check in date")

        if worked_hours and check_in and check_out:
            if worked_hours != (check_out - check_in).total_seconds()/3600:
                raise serializers.ValidationError("worked hours must be equal difference between check in and check out")

        
        if check_out and check_in and check_out <= check_in:
            raise serializers.ValidationError("The check_out date must be after the check_in date.")

        if check_out and check_in and check_out > (check_in + timedelta(hours=24)) :
            raise serializers.ValidationError("The check_out date cant be after 1 day of its check_in .")

        return data

    def validate_check_out(self,value):
        if not value:
            raise serializers.ValidationError('check out cannot be empty')

        return value      