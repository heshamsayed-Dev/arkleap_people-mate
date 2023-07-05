from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_model_by_pk


class LocationDeleteView(APIView):
    def delete(self, request, pk):
        try:
            location = get_model_by_pk("Location", pk)
            location.delete()
            return Response(data={"message": "Location deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
