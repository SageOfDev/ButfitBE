from django.urls import reverse

from rest_framework.test import APITestCase


class UserCreateAPIViewTestCase(APITestCase):
    url = reverse('mypage:join')

    def setUp(self):
        self.user_data = {
            'username':  "010-1234-1234",
            'password': "password",
            'confirm_password': "password"
        }

    def test_invalid_username(self):
        """
        회원가입 - useranme 에러
        """
        self.user_data['username'] = 'username123'
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(400, response.status_code)

    def test_invalid_password(self):
        """
        회원가입 - password 에러
        """
        self.user_data['confirm_password'] = 'invalid_passowrd'
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(400, response.status_code)

    def test_join(self):
        """
        회원가입 - 정상 가입
        """
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(201, response.status_code)

    def test_unique_username(self):
        """
        회원가입 - 중복가입
        """
        self.client.post(self.url, self.user_data)
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(400, response.status_code)
