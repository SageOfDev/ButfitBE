from django.urls import path

from mypage.views import *

app_name = "mypage"

urlpatterns = [
    path('join/', UserCreateAPIView.as_view(), name='join'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),

    path('credit/', CreditCreateAPIView.as_view(), name='credit-list'),
    path('credit/<int:pk>/', CreditUpdateAPIView.as_view(), name='credit-detail'),
]