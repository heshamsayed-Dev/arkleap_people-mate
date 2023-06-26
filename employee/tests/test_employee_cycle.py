from faker import Faker
from rest_framework.test import APITestCase

from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.employee_model import Employee

from .api_factory import CompanyBranchFactory, CompanyFactory, EmployeeFactory


class TestEmployeeCreation(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = CompanyFactory()
        cls.branch = CompanyBranchFactory(company=cls.company)
        cls.employee = EmployeeFactory(company=cls.company, branch=cls.branch)

    def test_create_company(self):
        self.assertEqual(Company.objects.count(), 1)

    def test_create_branch(self):
        self.assertEqual(CompanyBranch.objects.count(), 1)

    def test_create_employee(self):
        self.assertEqual(Employee.objects.count(), 1)

        #                     Company Test Cycle                    #

    def test_list_companies(self):
        response = self.client.get("/companies/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_company(self):
        response = self.client.get(f"/companies/{self.company.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_company_api(self):
        data = {"name": Faker().name(), "address": Faker().sentence()}
        response = self.client.post("/companies/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_company_patch(self):
        response = self.client.patch(
            f"/companies/{self.company.id}/update", data={"name": Faker().name()}, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_company_put(self):
        data = {"name": Faker().name(), "address": Faker().sentence()}
        response = self.client.put(f"/companies/{self.company.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_company(self):
        response = self.client.delete(f"/companies/{self.company.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)

        #               Branch Test Cycle                  #

    def test_list_branches(self):
        response = self.client.get("/branches/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_branch(self):
        response = self.client.get(f"/branches/{self.branch.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_branch_api(self):
        data = {"name": Faker().name(), "address": Faker().sentence(), "company": self.company.id}
        response = self.client.post("/branches/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_branch_patch(self):
        data = {"name": Faker().name()}
        response = self.client.patch(f"/branches/{self.branch.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_branch_put(self):
        data = {"name": Faker().name(), "address": Faker().sentence(), "company": self.company.id}
        response = self.client.put(f"/branches/{self.branch.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_branch(self):
        response = self.client.delete(f"/branches/{self.branch.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)

        #               Employee Test Cycle               #

    def test_list_employees(self):
        response = self.client.get("/employees/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_employee(self):
        response = self.client.get(f"/employees/{self.employee.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_employee_api(self):
        data = {
            "name": Faker().name(),
            "email": Faker().email(),
            "mobile": Faker().random_number(digits=12),
            "department": "development",
            "position": "software_engineer",
            "branch": self.branch.id,
            "company": self.company.id,
        }
        response = self.client.post("/employees/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_employee_patch(self):
        data = {"name": Faker().name()}
        response = self.client.patch(f"/employees/{self.employee.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_employee_put(self):
        data = {
            "name": Faker().name(),
            "email": Faker().email(),
            "mobile": Faker().random_number(digits=12),
            "department": "development",
            "position": "software_engineer",
            "branch": self.branch.id,
            "company": self.company.id,
        }
        response = self.client.put(f"/employees/{self.employee.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_employee(self):
        response = self.client.delete(f"/employees/{self.employee.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)
