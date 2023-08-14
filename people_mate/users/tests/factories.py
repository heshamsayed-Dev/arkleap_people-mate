# from collections.abc import Sequence
# from typing import Any

from datetime import datetime

import pyotp
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from factory import post_generation
from factory.django import DjangoModelFactory
from faker import Faker

from employee.models.company_model import Company


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker().name()
    arabic_name = "بطه"
    tax_number = Faker().random_number(digits=15)
    commercial_record = Faker().random_number(digits=12)
    address = Faker().sentence()
    phone = Faker().random_number(digits=9)
    mobile = Faker().random_number(digits=12)
    fax = Faker().random_number(digits=6)
    email = Faker().email()
    country = Faker().name()
    slug = slugify(name)
    start_date = datetime.today().date()


class UserFactory(DjangoModelFactory):
    username = Faker().name()
    email = Faker().email()
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
            self.companies.add(extracted)

    #         # for company in extracted:
    #         #     self.companies.add(company)

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
