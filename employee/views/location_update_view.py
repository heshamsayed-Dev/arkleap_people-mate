from datetime import datetime

from django.http import Http404, QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.models.company_branch_model import CompanyBranch
from employee.serializers.location_serializer import LocationSerializer

from .utils import get_model_by_pk


class LocationUpdateView(APIView):
    def check_branch_locations_with_current_status(self, branch_id, location_id):
        branch = CompanyBranch.objects.prefetch_related("locations").get(id=branch_id)
        if branch.locations.filter(status="current").exists():
            current_location = branch.locations.filter(status="current").first()
            return current_location
        else:
            return None

    def put(self, request, pk):
        try:
            location = get_model_by_pk("Location", pk)
            data = request.data
            query_dict = QueryDict("", mutable=True)
            query_dict.update(request.data)
            query_dict["updated_at"] = datetime.now()
            serializer = LocationSerializer(location, data=query_dict)

            if serializer.is_valid():
                if data["status"] == "current":
                    current_location = self.check_branch_locations_with_current_status(data["branch"], pk)
                    if current_location:
                        if current_location.id != pk:
                            current_location.status = "expired"
                            current_location.updated_at = datetime.now()
                            current_location.save()

                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            location = get_model_by_pk("Location", pk)
            data = request.data
            query_dict = QueryDict("", mutable=True)
            query_dict.update(request.data)
            query_dict["updated_at"] = datetime.now()
            serializer = LocationSerializer(location, data=query_dict, partial=True)

            if serializer.is_valid():
                if data.get("status") and data.get("status") == "current":
                    if data.get("branch"):
                        current_location = self.check_branch_locations_with_current_status(data["branch"], pk)
                    else:
                        current_location = self.check_branch_locations_with_current_status(location.branch.id, pk)

                    if current_location:
                        if current_location.id != pk:
                            current_location.status = "expired"
                            current_location.updated_at = datetime.now()
                            current_location.save()
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
