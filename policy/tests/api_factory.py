from factory.django import DjangoModelFactory
from faker import Faker

from policy.models.policy_model import Policy


class PolicyFactory(DjangoModelFactory):
    class Meta:
        model = Policy

    working_hours = Faker().name()
    address = Faker().sentence()
