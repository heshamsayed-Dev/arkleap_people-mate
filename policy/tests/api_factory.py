import factory
from factory.django import DjangoModelFactory
from faker import Faker

from employee.tests.api_factory import CompanyFactory
from policy.models.policy_model import Policy


class PolicyFactory(DjangoModelFactory):
    class Meta:
        model = Policy

    company = factory.SubFactory(CompanyFactory)
    working_hours = Faker().random_number()
    working_policy_start_date = Faker().time()
    working_policy_end_date = Faker().time()
