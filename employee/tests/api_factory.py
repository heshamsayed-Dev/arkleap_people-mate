from datetime import datetime

import factory
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from faker import Faker

from employee.constants import STATUS_CURRENT
from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.department_model import Department
from employee.models.employee_model import Employee
from employee.models.location_model import Location
from employee.models.position_model import Position
from people_mate.users.models import User
from policy.models.policy_model import Policy


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker().name()
    password = make_password("123")
    is_active = True


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker().name()
    arabic_name = "بطه"
    tax_number = Faker().random_number(digits=15)
    commercial_record = Faker().random_number(digits=12)
    address = Faker().sentence()
    phone = Faker().random_number(digits=9)
    mobile = Faker().random_number(digits=12)
    fax = Faker().random_number(digits=6)
    email = Faker().email()
    country = Faker().name()
    slug = slugify(name)
    start_date = datetime.today().date()


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
    status = STATUS_CURRENT
    branch = factory.SubFactory(CompanyBranchFactory)


class PolicyFactory(DjangoModelFactory):
    class Meta:
        model = Policy

    company = factory.SubFactory(CompanyFactory)
    working_hours = 8
    working_policy_start_date = Faker().time("10")
    working_policy_end_date = Faker().time("18")


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
    policy = factory.SubFactory(PolicyFactory)
    user = factory.SubFactory(UserFactory)
