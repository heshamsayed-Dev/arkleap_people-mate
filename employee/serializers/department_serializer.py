from rest_framework import serializers

from employee.models.department_model import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
