from datetime import datetime

from django.http import Http404, QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.serializers.attendance_detail_serializer import AttendanceDetailSerializer

from .utils import get_model_by_pk


class AttendanceDetailUpdateView(APIView):
    def put(self, request, pk):
        try:
            attendance_detail = get_model_by_pk("AttendanceDetail", pk)
            query_dict = QueryDict("", mutable=True)
            query_dict.update(request.data)
            query_dict["updated_at"] = datetime.now()
            serializer = AttendanceDetailSerializer(attendance_detail, data=query_dict)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            attendance_detail = get_model_by_pk("AttendanceDetail", pk)
            query_dict = QueryDict("", mutable=True)
            query_dict.update(request.data)
            query_dict["updated_at"] = datetime.now()
            serializer = AttendanceDetailSerializer(attendance_detail, data=query_dict, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
