import json

from django.contrib.auth.models import User
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


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse('mypage:login')

    @classmethod
    def setUpTestData(cls):
        """
        셋업 - 유저 생성
        """
        cls.user = User.objects.create_user(username='010-1111-1111', password='password')

    def test_authetication_without_password(self):
        """
        로그인 - 패스워드 미입력
        """
        response = self.client.post(self.url, {'username': self.user.username})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        """
        로그인 - 틀린 패스워드
        """
        response = self.client.post(self.url, {'username': self.user.username, 'password': 'wrong'})
        self.assertEqual(400, response.status_code)

    def test_authentication(self):
        """
        로그인 - 정상 로그인
        """
        response = self.client.post(self.url, {'username': '010-1111-1111', 'password': 'password'})
        self.assertEqual(200, response.status_code)
        self.assertTrue('token' in json.loads(response.content))
