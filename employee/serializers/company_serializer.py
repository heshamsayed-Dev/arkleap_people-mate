import re
from datetime import datetime

from rest_framework import serializers

from employee.models.company_model import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    def validate_arabic_name(self, value):
        pattern = r"^[\u0621-\u063A\u0641-\u064A]+$"
        if not re.match(pattern, value):
            raise serializers.ValidationError("arabic name must be in arabic")

        return value

    def validate_start_date(self, value):
        today = datetime.today().date()
        if value > today:
            raise serializers.ValidationError("start date cannot be in the future")

        return value

    def validate_end_date(self, value):
        today = datetime.today().date()
        if value < today:
            raise serializers.ValidationError("end date cannot be in the past")

        return value
