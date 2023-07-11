from faker import Faker
from rest_framework.test import APITestCase

from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.department_model import Department
from employee.models.employee_model import Employee
from employee.models.location_model import Location
from employee.models.position_model import Position
from attendance.models.attendance_detail_model import AttendanceDetail
from attendance.models.attendance_model import Attendance
from datetime import datetime
from employee.tests.utils import set_authentication_token
from .api_factory import (
    UserFactory,
    CompanyBranchFactory,
    CompanyFactory,
    DepartmentFactory,
    EmployeeFactory,
    LocationFactory,
    PositionFactory,
    AttendanceFactory,
    AttendanceDetailFactory,
)


class TestAttendanceCreation(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user=UserFactory()
        cls.company = CompanyFactory()
        cls.branch = CompanyBranchFactory(company=cls.company)
        cls.location = LocationFactory(branch=cls.branch)
        cls.position = PositionFactory(company=cls.company)
        cls.department = DepartmentFactory(company=cls.company)
        cls.employee = EmployeeFactory(
            company=cls.company, branch=cls.branch, department=cls.department, position=cls.position,user=cls.user
        )
        cls.attendance=AttendanceFactory(employee=cls.employee)
        cls.attendance_detail=AttendanceDetailFactory(branch=cls.branch,attendance=cls.attendance)

    def test_create_company(self):
        self.assertEqual(Company.objects.count(), 1)

    def test_create_branch(self):
        self.assertEqual(CompanyBranch.objects.count(), 1)

    def test_create_location(self):
        self.assertEqual(Location.objects.count(), 1)

    def test_create_department(self):
        self.assertEqual(Department.objects.count(), 1)

    def test_create_position(self):
        self.assertEqual(Position.objects.count(), 1)

    def test_create_employee(self):
        self.assertEqual(Employee.objects.count(), 1)

    def test_create_attendance(self):
        self.assertEqual(Attendance.objects.count(), 1)

    def test_create_attendance_detail(self):
        self.assertEqual(AttendanceDetail.objects.count(), 1)


        #####   Attendance test #######

    def test_list_attendances(self):
        set_authentication_token(self)
        response = self.client.get("/attendances/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_attendance(self):
        set_authentication_token(self)
        response = self.client.get(f"/attendances/{self.attendance.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_calculate_attendance(self):
        set_authentication_token(self)
        response = self.client.get(f"/attendances/{self.attendance.id}/calculate", format="json")
        self.assertEqual(response.status_code, 200)    

    def test_create_attendance_api(self):
        set_authentication_token(self)
        data = {
            "employee": self.employee.id,
            "check_in": datetime.now(),
            "date": datetime.today().date(),
        }
        response = self.client.post("/attendances/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_attendance_patch(self):
        set_authentication_token(self)
        data = {"check_in": datetime(2023, 5, 9, 8, 30, 0, 123456)}
        response = self.client.patch(f"/attendances/{self.attendance.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_attendance_put(self):
        set_authentication_token(self)
        data = {
            "check_in": datetime(2023, 5, 9, 9, 30, 0, 123456),
            "date": self.attendance.check_in.date(),
            "check_out": datetime(2023, 5, 9, 15, 30, 0, 123456),
            "employee":self.employee.id,
            "worked_hours":6.0,
            "shift_start_time":9.30,
            "shift_end_time":15.30,
        }
        response = self.client.put(f"/attendances/{self.attendance.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_attendance(self):
        set_authentication_token(self)
        response = self.client.delete(f"/attendances/{self.attendance.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)   



        #####   Attendance Details test #######
        
    def test_list_attendance_details(self):
        set_authentication_token(self)
        response = self.client.get("/attendance-details/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_attendance_detail(self):
        set_authentication_token(self)
        response = self.client.get(f"/attendance-details/{self.attendance_detail.id}", format="json")
        self.assertEqual(response.status_code, 200)
    

    def test_create_attendance_detail_api(self):
        set_authentication_token(self)
        data = {
            "branch": self.branch.id,
            "check_in": datetime(2023, 5, 9, 7, 30, 0, 123456),
            "check_out":datetime(2023, 5, 9, 10, 30, 0, 123456)
        }
        response = self.client.post("/attendance-details/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_attendance_detail_patch(self):
        set_authentication_token(self) 
        data = {"check_in": datetime(2023, 5, 9, 8, 30, 0, 123456)}
        response = self.client.patch(f"/attendance-details/{self.attendance_detail.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_attendance_detail_put(self):
        set_authentication_token(self)
        data = {
            "branch":self.branch.id,
            "check_in":datetime(2023, 5, 9, 9, 30, 0, 123456),
            "check_out": datetime(2023, 5, 9, 15, 30, 0, 123456),
        }
        response = self.client.put(f"/attendance-details/{self.attendance_detail.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_attendance_detail(self):
        set_authentication_token(self)
        response = self.client.delete(f"/attendance-details/{self.attendance_detail.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)          


