from factory.django import DjangoModelFactory
from faker import Faker
import faker
import factory
from policy.models.policy_model import Policy
from employee.tests.api_factory import CompanyFactory


class PolicyFactory(DjangoModelFactory):
    class Meta:
        model = Policy

    company = factory.SubFactory(CompanyFactory)
    working_hours = Faker().random_number()
    # working_policy_start_date= faker.date.anytime() 
    # working_policy_end_date= faker.date.anytime() 

    # working_policy_end_date= Faker("time_object")
    working_policy_start_date= Faker().time()
    working_policy_end_date= Faker().time()

    
