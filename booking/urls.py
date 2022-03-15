from django.urls import path

from booking.views import BookingCreateAPIView, PaymentCreateAPIView, BookingUpdateAPIView

urlpatterns = [
    path('', BookingCreateAPIView.as_view(), name='booking-list'),
    path('<int:booking_id>/payment/', PaymentCreateAPIView.as_view(), name='payment-list'),
    path('<int:pk>/', BookingUpdateAPIView.as_view(), name='booking-detail'),
]