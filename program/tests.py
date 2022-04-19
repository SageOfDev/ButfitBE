from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from datetime import date


class ProgramCreateAPIViewTestCase(APITestCase):
    url = reverse('program:list')

    def test_with_normal_user(self):
        user = User.objects.create_user(username="010-1111-1111", password="password")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(self.url,
                                    {
                                        "location": "DG",
                                        "name": "상체",
                                        "price": 180000,
                                        "capacity": 1,
                                        "date": str(date.today()),
                                        "start_time": "10:00:00",
                                        "end_time": "11:00:00"
                                    })
        self.assertEqual(403, response.status_code)

    def test_with_superuser(self):
        user = User.objects.create_superuser(username="010-1111-1111", password="password")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(self.url,
                                    {
                                        "location": "DG",
                                        "name": "상체",
                                        "price": 180000,
                                        "capacity": 1,
                                        "date": str(date.today()),
                                        "start_time": "10:00:00",
                                        "end_time": "11:00:00"
                                    })
        self.assertEqual(201, response.status_code)
