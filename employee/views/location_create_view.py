from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.constants import STATUS_CURRENT, STATUS_EXPIRED
from employee.models.company_branch_model import CompanyBranch
from employee.serializers.location_serializer import LocationSerializer


class LocationCreateView(APIView):
    def post(self, request):
        data = request.data
        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            branch = CompanyBranch.objects.prefetch_related("locations").get(id=data["branch"])

            if data["status"] == STATUS_CURRENT and branch.locations.filter(status=STATUS_CURRENT).exists():
                current_location = branch.locations.filter(status=STATUS_CURRENT).first()
                current_location.status = STATUS_EXPIRED
                current_location.updated_at = datetime.now()
                current_location.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
