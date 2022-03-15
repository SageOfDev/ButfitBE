from django.urls import path

from mypage.views import CreditCreateAPIView, CreditUpdateAPIView

urlpatterns = [
    path('credit/', CreditCreateAPIView.as_view(), name='credit-post'),
    path('credit/<int:pk>', CreditUpdateAPIView.as_view(), name='credit-update'),

]