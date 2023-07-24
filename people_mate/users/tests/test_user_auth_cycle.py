from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APITestCase

from .factories import UserFactory

User = get_user_model()


class TestAttendanceCreation(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)

    def test_user_signup(self):
        password = Faker().password()
        user_data = {
            "username": Faker().name()[0],
            "email": Faker().email(),
            "password": password,
            "password_confirm": password,
        }
        response = self.client.post("/api/signup", data=user_data)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        user_credentials = {
            "email": self.user.email,
            "password": "123Aa$bb",
        }
        response = self.client.post("/api/login", data=user_credentials)
        self.assertEqual(response.status_code, 200)
