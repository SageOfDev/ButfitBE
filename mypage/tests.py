import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase


class UserCreateAPIViewTestCase(APITestCase):
    url = reverse('mypage:join')

    def setUp(self):
        self.user_data = {
            'username':  "010-1111-1111",
            'password': "password",
            'confirm_password': "password"
        }

    def test_invalid_username(self):
        """
        회원가입 - username 형식 에러
        """
        self.user_data['username'] = 'username111'
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(400, response.status_code)

    def test_invalid_password(self):
        """
        회원가입 - password 불일치
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
        self.assertTrue('token' in json.loads(response.content))

    def test_unique_username(self):
        """
        회원가입 - 중복가입
        """
        self.client.post(self.url, self.user_data)
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    join_url = reverse("mypage:join")
    url = reverse('mypage:login')

    def setUp(self):
        """
        셋업 - 유저 생성
        """
        self.user = {'username': '010-1111-1111', 'password': 'password', 'confirm_password': 'password'}
        response = self.client.post(self.join_url, self.user)
        self.assertEqual(201, response.status_code)
        del self.user['confirm_password']

    def test_without_password(self):
        """
        로그인 - 패스워드 미입력
        """
        response = self.client.post(self.url, {'username': self.user['username']})
        self.assertEqual(400, response.status_code)

    def test_with_wrong_password(self):
        """
        로그인 - 틀린 패스워드
        """
        response = self.client.post(self.url, {'username': self.user['username'], 'password': 'wrong'})
        self.assertEqual(400, response.status_code)

    def test_authentication(self):
        """
        로그인 - 정상 로그인
        """
        response = self.client.post(self.url, self.user)
        self.assertEqual(200, response.status_code)
        self.assertTrue('token' in json.loads(response.content))

    def test_inactive_user(self):
        """
        로그인 - 비활성 유저
        """
        user = User.objects.get(username=self.user['username'])
        user.is_active = False
        user.save()
        response = self.client.post(self.url, self.user)
        self.assertEqual(400, response.status_code)


class UserLogoutAPIViewTestCase(APITestCase):
    join_url =  reverse('mypage:join')
    login_url = reverse('mypage:login')
    url = reverse('mypage:logout')

    def setUp(self):
        """
        셋업 - 유저 생성 + 로그인
        """
        self.user = {'username': '010-1111-1111', 'password': 'password', 'confirm_password': 'password'}
        response = self.client.post(self.join_url, self.user)
        self.assertEqual(201, response.status_code)
        self.token = Token.objects.last().key

        del self.user['confirm_password']
        response = self.client.post(self.login_url, self.user)
        self.assertEqual(200, response.status_code)

    def test_with_wrong_token(self):
        """
        로그아웃 - 비정상 토큰
        """
        pre_token_cnt = Token.objects.all().count()
        response = self.client.post(self.url, {'token': 'wrong_token'})
        token_cnt = Token.objects.all().count()
        self.assertEqual(400, response.status_code)
        self.assertEqual(pre_token_cnt, token_cnt)

    def test_logout(self):
        """
        로그아웃 - 정상 토큰
        """
        pre_token_cnt = Token.objects.all().count()
        response = self.client.post(self.url, {'token': self.token})
        token_cnt = Token.objects.all().count()
        self.assertEqual(204, response.status_code)
        self.assertEqual(pre_token_cnt - 1, token_cnt)

    def test_with_inactive_user(self):
        """
        로그아웃 - 정상 토큰 & 비활성 계정
        """
        user = User.objects.get(username=self.user['username'])
        user.is_active = False
        user.save()
        pre_token_cnt = Token.objects.all().count()
        response = self.client.post(self.url, {'token': self.token})
        token_cnt = Token.objects.all().count()
        self.assertEqual(400, response.status_code)
        self.assertEqual(pre_token_cnt, token_cnt)
