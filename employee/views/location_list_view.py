from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.models.location_model import Location
from employee.serializers.location_serializer import LocationSerializer

from .utils import get_model_by_pk


class LocationListView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                location = get_model_by_pk("Location", pk)
                serializer = LocationSerializer(location)
            else:
                locations = Location.objects.all()
                serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data)

        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
