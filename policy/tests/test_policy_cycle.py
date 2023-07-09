from faker import Faker
from rest_framework.test import APITestCase
from ..models.policy_model import Policy
from .api_factory import (PolicyFactory)
from employee.tests.api_factory import CompanyFactory


class TestPolicy(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = CompanyFactory()
        cls.policy = PolicyFactory(company=cls.company)
      

    def test_create_policy(self):
        self.assertEqual(Policy.objects.count(), 1)


    def test_list_policies(self):
        response = self.client.get("/policy/", format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_policy(self):
        response = self.client.get(f"/policy/{self.policy.id}", format="json")
        self.assertEqual(response.status_code, 200)

    def test_create_policy_api(self):
        data = {"working_hours": Faker().random_number(), "working_policy_start_date": Faker().time(),"working_policy_end_date": Faker().time()}
        response = self.client.post("/policy/create", data=data, format="json")
        self.assertEqual(response.status_code, 201)


    def test_update_policy(self):
        data = {"working_hours": Faker().random_number()}
        response = self.client.put(f"/policy/{self.policy.id}/update", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_policy(self):
        response = self.client.delete(f"/policy/{self.policy.id}/delete", format="json")
        self.assertEqual(response.status_code, 204)
