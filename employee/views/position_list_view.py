from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.models.position_model import Position
from employee.serializers.position_serializer import PositionSerializer

from .utils import get_model_by_pk


class PositionListView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                position = get_model_by_pk("Position", pk)
                serializer = PositionSerializer(position)
            else:
                positions = Position.objects.all()
                serializer = PositionSerializer(positions, many=True)
            return Response(serializer.data)

        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
