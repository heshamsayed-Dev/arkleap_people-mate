from rest_framework.test import APITestCase
from rest_framework import status
from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.employee_model import Employee
from faker import Faker
from django.urls import reverse
from .test_utils import test_create_branch , test_create_company , test_create_employee

class CompanyTests(APITestCase):
    def SetUpClass()
    def setUp(self):
        self.company = test_create_company(self,
            {'name':Faker().name(),
            'address':Faker().sentence()})

        self.branch1 = test_create_branch(self,
            {
                'name':Faker().name(),
                'address':Faker().sentence(),
                'company':self.company.id
            })

        self.branch2 = test_create_branch(self,
            {
                'name':Faker().name(),
                'address':Faker().sentence(),
                'company':self.company.id
            })
        self.employee1 = test_create_employee(self,
            {
                'name':Faker().name(),
                'email':Faker().name(),
                'position':'software_engineer',
                'department':'development',
                'mobile':Faker().random_number(digits=5),
                'company':self.company.id,
                'branch':self.branch1.id
            })
        self.employee2 = test_create_employee(self,
            {
                'name':Faker().name(),
                'email':Faker().name(),
                'position':'software_engineer',
                'department':'development',
                'mobile':Faker().random_number(digits=5),
                'company':self.company.id,
                'branch':self.branch1.id
            })
        self.employee3 = test_create_employee(self,
            {
                'name':Faker().name(),
                'email':Faker().name(),
                'position':'software_engineer',
                'department':'development',
                'mobile':Faker().random_number(digits=5),
                'company':self.company.id,
                'branch':self.branch2.id
            })

    #test relation between company and employees
    def test_retrieve_employees_for_company(self):
        employees = Employee.objects.filter(company=self.company)
        self.assertEqual(employees.count(), 3)
        for employee in employees:
            self.assertEqual(employee.company, self.company)

    #test relation between branch and employees
    def test_retrieve_employees_for_branch(self):
        employees = Employee.objects.filter(branch=self.branch1)
        self.assertEqual(employees.count(), 2)
        for employee in employees:
            self.assertEqual(employee.branch, self.branch1)

    #test update company using the update company api and compare it with
    #company details from branch
    #company details from employee
    def test_update_company_details(self):
        data={'name':Faker().name()}
        response = self.client.patch(reverse('company_update', args=[self.company.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        branches = CompanyBranch.objects.filter(company=self.company)
        for branch in branches:
            self.assertEqual(branch.company.name, data['name'])
        employees = Employee.objects.filter(company=self.company)
        for employee in employees:
            self.assertEqual(employee.company.name,  data['name'])

    #test update branch using the update branch api and compare it with
    #branch details from employee
    def test_update_branch_details(self):
        data={'name':Faker().name(),'address':Faker().sentence()}
        response = self.client.patch(reverse('branch_update', args=[self.branch1.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        employees = Employee.objects.filter(branch=self.branch1)
        for employee in employees:
            self.assertEqual(employee.branch.name,  data['name'])
            self.assertEqual(employee.branch.address,  data['address'])        

    #test delete company api and check for employees and branches to be deleted 
    def test_delete_company(self):
       response = self.client.delete(reverse('company_delete', args=[self.company.id]))
       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
       self.assertEqual(Company.objects.count(), 0)
       self.assertEqual(CompanyBranch.objects.count(), 0)
       self.assertEqual(Employee.objects.count(), 0)


    # #test delete branch api and check for employees to be deleted 
    def test_delete_branch(self):
       response = self.client.delete(reverse('company_delete', args=[self.company.id]))
       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
       self.assertEqual(CompanyBranch.objects.count(), 0)
       self.assertEqual(Employee.objects.count(), 0)

    def tearDown(self):
        self.employee1.delete()
        self.employee2.delete()
        self.employee3.delete()
        self.branch1.delete()
        self.branch2.delete()
        self.company.delete()    




    
