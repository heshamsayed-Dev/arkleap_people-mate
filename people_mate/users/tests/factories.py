# from collections.abc import Sequence
# from typing import Any

import pyotp
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# from factory import Faker, post_generation
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from employee.models.company_model import Company


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker("name")
    address = Faker("address")


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    # name = Faker("name")
    is_active = True
    role = "employee"
    password = make_password("123Aa$bb")
    otp_secret = pyotp.random_base32()
    company = CompanyFactory()

    @post_generation
    def companies(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for company in extracted:
                self.companies.add(company)

    # @post_generation
    # def password(self, create: bool, extracted: Sequence[Any], **kwargs):
    #     password = (
    #         extracted
    #         if extracted
    #         else Faker(
    #             "password",
    #             length=42,
    #             special_chars=True,
    #             digits=True,
    #             upper_case=True,
    #             lower_case=True,
    #         ).evaluate(None, None, extra={"locale": None})
    #     )
    #     self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
