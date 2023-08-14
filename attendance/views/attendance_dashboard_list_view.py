# from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models.attendance_model import Attendance
from attendance.serializers.attendance_dashboard_serializer import DashboardSerializer
from employee.models.company_branch_model import CompanyBranch
from employee.models.employee_model import Employee


class AttendanceDashboardListView(APIView):
    def get(self, request):
        # company=request.user.company
        company = 1
        employees_count = Employee.objects.filter(company=company).count()
        branches_count = CompanyBranch.objects.filter(company=company).count()
        permissions_count = 0
        attendances_count = Attendance.objects.filter(company=company).count()
        attendances = Attendance.objects.filter(company=company)

        # paginator = Paginator(attendances, per_page=10)
        # page_number = request.GET.get('page')

        paginator = LimitOffsetPagination()
        paginated_attendances = paginator.paginate_queryset(attendances, request)
        # paginated_attendances= paginator.get_page(page_number)
        # serializer = AttendanceSerializer(paginated_attendances, many=True)
        serializer = DashboardSerializer(
            {
                "num_employees": employees_count,
                "num_branches": branches_count,
                "num_attendances": permissions_count,
                "num_permissions": attendances_count,
                "attendances": paginated_attendances,
            }
        )
        return Response(serializer.data)
