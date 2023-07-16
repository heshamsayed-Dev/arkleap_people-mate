from faker import Faker
from rest_framework.test import APITestCase

from employee.constants import STATUS_CURRENT, STATUS_EXPIRED
from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.department_model import Department
from employee.models.employee_model import Employee
from employee.models.location_model import Location
from employee.models.position_model import Position
from people_mate.users.models import User

from .api_factory import (
    CompanyBranchFactory,
    CompanyFactory,
    DepartmentFactory,
    EmployeeFactory,
    LocationFactory,
    PositionFactory,
    UserFactory,
)

# from django.contrib.auth.models import User
from .utils import set_authentication_token


class TestEmployeeCreation(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.company = CompanyFactory()
        cls.branch = CompanyBranchFactory(company=cls.company)
        cls.location = LocationFactory(branch=cls.branch)
        cls.position = PositionFactory(company=cls.company)
        cls.department = DepartmentFactory(company=cls.company)

        cls.employee = EmployeeFactory(
            company=cls.company, branch=cls.branch, department=cls.department, position=cls.position, user=cls.user
        )

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)

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

        #                     Company Test Cycle                    #

    def test_list_companies(self):
        set_authentication_token(self)
        response = self.client.get("/companies/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_company(self):
        set_authentication_token(self)
        response = self.client.get(f"/companies/{self.company.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_company_api(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "address": Faker().sentence()}
        response = self.client.post("/companies/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_company_patch(self):
        set_authentication_token(self)
        response = self.client.patch(
            f"/companies/{self.company.id}/update", data={"name": Faker().name()}, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_company_put(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "address": Faker().sentence()}
        response = self.client.put(f"/companies/{self.company.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_company(self):
        set_authentication_token(self)
        response = self.client.delete(f"/companies/{self.company.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)

        #               Branch Test Cycle                  #

    def test_list_branches(self):
        set_authentication_token(self)
        response = self.client.get("/branches/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_branch(self):
        set_authentication_token(self)
        response = self.client.get(f"/branches/{self.branch.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_branch_api(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "address": Faker().sentence(), "company": self.company.id}
        response = self.client.post("/branches/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_branch_patch(self):
        set_authentication_token(self)
        data = {"name": Faker().name()}
        response = self.client.patch(f"/branches/{self.branch.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_branch_put(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "address": Faker().sentence(), "company": self.company.id}
        response = self.client.put(f"/branches/{self.branch.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_branch(self):
        set_authentication_token(self)
        response = self.client.delete(f"/branches/{self.branch.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)

        #               Location Test Cycle                  #

    def test_list_locations(self):
        set_authentication_token(self)
        response = self.client.get("/locations/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_location(self):
        set_authentication_token(self)
        response = self.client.get(f"/locations/{self.location.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_location_api(self):
        set_authentication_token(self)
        data = {
            "longitude": Faker().random.uniform(-180.0, 180.0),
            "latitude": Faker().random.uniform(-90.0, 90.0),
            "status": "current",
            "branch": self.branch.id,
        }
        response = self.client.post("/locations/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_location_patch(self):
        set_authentication_token(self)
        data = {"status": STATUS_EXPIRED}
        response = self.client.patch(f"/locations/{self.location.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_location_put(self):
        set_authentication_token(self)
        data = {
            "longitude": Faker().random.uniform(-180.0, 180.0),
            "latitude": Faker().random.uniform(-90.0, 90.0),
            "status": STATUS_CURRENT,
            "branch": self.branch.id,
        }
        response = self.client.put(f"/locations/{self.location.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_location(self):
        set_authentication_token(self)
        response = self.client.delete(f"/locations/{self.location.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)

        #               Department Test Cycle                  #

    def test_list_departments(self):
        set_authentication_token(self)
        response = self.client.get("/departments/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_department(self):
        set_authentication_token(self)
        response = self.client.get(f"/departments/{self.department.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_department_api(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "company": self.company.id}
        response = self.client.post("/departments/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_department_patch(self):
        set_authentication_token(self)
        data = {"name": Faker().name()}
        response = self.client.patch(f"/departments/{self.department.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_department_put(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "address": Faker().sentence(), "company": self.company.id}
        response = self.client.put(f"/departments/{self.department.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_department(self):
        set_authentication_token(self)
        response = self.client.delete(f"/departments/{self.department.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)

        #               Position Test Cycle                  #

    def test_list_positions(self):
        set_authentication_token(self)
        response = self.client.get("/positions/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_position(self):
        set_authentication_token(self)
        response = self.client.get(f"/positions/{self.position.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_position_api(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "company": self.company.id}
        response = self.client.post("/positions/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_position_patch(self):
        set_authentication_token(self)
        data = {"name": Faker().name()}
        response = self.client.patch(f"/positions/{self.position.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_position_put(self):
        set_authentication_token(self)
        data = {"name": Faker().name(), "address": Faker().sentence(), "company": self.company.id}
        response = self.client.put(f"/positions/{self.position.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_position(self):
        set_authentication_token(self)
        response = self.client.delete(f"/positions/{self.position.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)

        #               Employee Test Cycle               #

    def test_list_employees(self):
        set_authentication_token(self)
        response = self.client.get("/employees/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_employee(self):
        set_authentication_token(self)
        response = self.client.get(f"/employees/{self.employee.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_employee_api(self):
        set_authentication_token(self)
        user = User.objects.create(username=Faker().name(), password="123")
        data = {
            "name": Faker().name(),
            "email": Faker().email(),
            "mobile": Faker().random_number(digits=12),
            "department": self.department.id,
            "position": self.position.id,
            "branch": self.branch.id,
            "company": self.company.id,
            "user": user.id,
        }
        response = self.client.post("/employees/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_employee_patch(self):
        set_authentication_token(self)
        data = {"name": Faker().name()}
        response = self.client.patch(f"/employees/{self.employee.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_employee_put(self):
        set_authentication_token(self)
        data = {
            "name": Faker().name(),
            "email": Faker().email(),
            "mobile": Faker().random_number(digits=12),
            "department": self.department.id,
            "position": self.position.id,
            "branch": self.branch.id,
            "company": self.company.id,
            "user": self.user.id,
        }
        response = self.client.put(f"/employees/{self.employee.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_employee(self):
        set_authentication_token(self)
        response = self.client.delete(f"/employees/{self.employee.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)
