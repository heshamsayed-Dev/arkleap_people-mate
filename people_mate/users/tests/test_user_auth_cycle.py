import pyotp
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APITestCase

from .factories import CompanyFactory, UserFactory
from .utils import set_authentication_token

User = get_user_model()


class TestAttendanceCreation(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_1 = CompanyFactory()
        cls.company_2 = CompanyFactory()
        cls.user = UserFactory(companies=(cls.company_1, cls.company_2), company=cls.company_2)
        cls.totp = pyotp.TOTP(cls.user.otp_secret, interval=30)

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_api(self):
        set_authentication_token(self)
        password = Faker().password()
        user_data = {
            "username": Faker().name()[0],
            "email": Faker().email(),
            "password": password,
            "password_confirm": password,
        }
        response = self.client.post("/users/create", data=user_data)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        user_credentials = {
            "email": self.user.email,
            "password": "123Aa$bb",
            "otp": self.totp.now(),
        }
        response = self.client.post("/api/login", data=user_credentials)

        self.assertEqual(response.status_code, 200)

    def test_reset_password_send_email(self):
        data = {"email": self.user.email}
        response = self.client.post("/users/reset-password/send-email", data=data)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_validate_otp(self):
        data = {"otp": self.totp.now()}
        response = self.client.post(f"/users/{self.user.id}/reset-password/validate-otp", data=data)
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        set_authentication_token(self)
        data = {
            "password": "123Aa$bb3",
            "password_confirm": "123Aa$bb3",
        }
        response = self.client.post("/users/reset-password", data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        set_authentication_token(self)
        data = {"companies": self.company_1.id}
        response = self.client.patch(f"/users/{self.user.id}/update", data=data)
        self.assertEqual(response.status_code, 200)

    def test_activate_user_company(self):
        set_authentication_token(self)
        response = self.client.post(f"/users/activate-company/{self.company_1.id}")
        self.assertEqual(response.status_code, 200)
