from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.serializers.location_serializer import LocationSerializer


class LocationCreateView(APIView):
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
