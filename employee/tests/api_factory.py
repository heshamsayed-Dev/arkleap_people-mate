import factory
from factory.django import DjangoModelFactory
from employee.models.company_branch_model import CompanyBranch
from employee.models.company_model import Company
from employee.models.employee_model import Employee
from faker import Faker

class CompanyFactory(DjangoModelFactory):
    class Meta:
        model=Company

    name=Faker().name()
    address=Faker().sentence()



class CompanyBranchFactory(DjangoModelFactory):
    class Meta:
        model=CompanyBranch
    
    name=Faker().name()
    address=Faker().sentence()
    company=factory.SubFactory(CompanyFactory)


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model=Employee

    name=Faker().name()
    email=Faker().name()
    mobile=Faker().random_number(digits=5)
    department='development'
    position='software_engineer'
    company=factory.SubFactory(CompanyFactory)
    branch=factory.SubFactory(CompanyBranchFactory)  




    


