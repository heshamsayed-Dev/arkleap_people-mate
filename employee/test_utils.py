from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.employee_model import Employee
from django.urls import reverse

   # test api that creates company
def test_create_company(self,company):
       
        response=self.client.post(reverse('company_create'),company)
        self.assertEqual(response.status_code, 201)
        company=Company.objects.filter(id=response.data['id']).first()
        return company
    # test api that creates branch
def test_create_branch(self,branch):
        response=self.client.post(reverse('branch_create'),branch)
        self.assertEqual(response.status_code,201)
        branch=CompanyBranch.objects.filter(id=response.data['id']).first()
        return branch

    # test api that creates employee
def test_create_employee(self,employee):
        response=self.client.post(reverse('employee_create'),employee)
        self.assertEqual(response.status_code, 201)
        employee=Employee.objects.filter(id=response.data['id']).first()
        return employee        