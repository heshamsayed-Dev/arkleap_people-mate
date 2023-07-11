from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.signals import pre_save

from attendance.serializers.attendance_detail_serializer import AttendanceDetailSerializer


class AttendanceDetailCreateView(APIView):
    def post(self, request):
        # data = request.data.copy()
        # print(f"employee branch is {request.user.employee.branch}")
        # data['branch']=request.user.employee.branch
        # print(data)
        serializer = AttendanceDetailSerializer(data=request.data,context={"employee":request.user.employee})
        if serializer.is_valid():
            serializer.save()
           

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
