import factory
from factory.django import DjangoModelFactory
from faker import Faker
from attendance.models.attendance_model import Attendance
from attendance.models.attendance_detail_model import AttendanceDetail
from employee.models.employee_model import Employee
from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.location_model import Location
from employee.models.position_model import Position
from employee.models.department_model import Department
from people_mate.users.models import User
from django.contrib.auth.hashers import make_password

from datetime import datetime

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker().name()
    password = make_password('123')
    is_active=True


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker().name()
    address = Faker().sentence()


class CompanyBranchFactory(DjangoModelFactory):
    class Meta:
        model = CompanyBranch

    name = Faker().name()
    address = Faker().sentence()
    company = factory.SubFactory(CompanyFactory)


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    longitude = Faker().random.uniform(-180.0, 180.0)
    latitude = Faker().random.uniform(-90.0, 90.0)
    status = "current"
    branch = factory.SubFactory(CompanyBranchFactory)

class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = Faker().name()
    company = factory.SubFactory(CompanyFactory)


class PositionFactory(DjangoModelFactory):
    class Meta:
        model = Position

    name = Faker().name()
    company = factory.SubFactory(CompanyFactory)    

class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    name = Faker().name()
    email = Faker().name()
    mobile = Faker().random_number(digits=5)
    department = factory.SubFactory(DepartmentFactory)
    position = factory.SubFactory(PositionFactory)
    company = factory.SubFactory(CompanyFactory)
    branch = factory.SubFactory(CompanyBranchFactory)
    user=factory.SubFactory(UserFactory)


class AttendanceFactory(DjangoModelFactory):
    class Meta:
        model = Attendance
    employee = factory.SubFactory(EmployeeFactory)
    check_in=datetime(2023, 5, 9, 7, 30, 0, 123456)
    date=check_in.date()
    check_out = datetime(2023, 5, 9, 15, 30, 0, 123456)

class AttendanceDetailFactory(DjangoModelFactory):
    class Meta:
        model = AttendanceDetail
    branch=factory.SubFactory(CompanyBranchFactory)
    attendance=factory.SubFactory(AttendanceFactory)
    check_in=datetime(2023, 5, 9, 7, 30, 0, 123456)
    check_out = datetime(2023, 5, 9,15 , 30, 0, 123456)




