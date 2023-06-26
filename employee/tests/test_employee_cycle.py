from rest_framework.test import APITestCase

from .api_factory import CompanyFactory,CompanyBranchFactory,EmployeeFactory
from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.employee_model import Employee


class TestEmployeeCreation(APITestCase):


    @classmethod
    def SetUpClass(cls):
        super(TestEmployeeCreation,cls).SetUpClass()
        company=CompanyFactory()
        branch=CompanyBranchFactory(company=company)
        employee=EmployeeFactory(company=company,branch=branch)

    
    def test_create_company(self):
        self.assertEqual(Company.objects.count(),1)

    def test_create_branch(self):
        self.assertEqual(CompanyBranch.objects.count(),1)

    def test_create_employee(self):
        self.assertEqual(Employee.objects.count(),1)


            