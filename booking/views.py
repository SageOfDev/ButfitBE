from decimal import *
from datetime import date, timedelta


from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.models import Booking
from booking.serializers import BookingCreateSerializer, PaymentCreateSerializer, BookingUpdateSerializer, \
    PaymentUpdateSerializer
from mypage.models import Credit
from mypage.permissions import IsOwner
from program.models import Program


class BookingCreateAPIView(CreateAPIView):
    queryset = Booking
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        program = Program.objects.get(id=request.data.get('program'))

        # 중복 예약 점검
        if Booking.objects.filter(
            Q(program_id=program.id) &
            Q(customer__phone_number=request.data.get('customer')) &
            Q(status=Booking.PAID)
        ).exists():
            return Response({"message": "이미 예약된 수업입니다."}, status=status.HTTP_409_CONFLICT)

        # 정원 점검
        if len(Booking.objects.filter(
            Q(program_id=program.id) &
            Q(status=Booking.PAID)
        )) >= program.capacity:
            return Response({"message": "정원 초과입니다."}, status=status.HTTP_409_CONFLICT)

        self.perform_create(serializer)
        # TODO 아래 절대 경로 바꾸기
        headers = {'Location': 'http://127.0.0.1:8000/booking/%s/payment/' % serializer.data['id']}
        return Response(serializer.data, status=status.HTTP_307_TEMPORARY_REDIRECT, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)

        credit_list = Credit.objects.filter(
            Q(customer__phone_number=booking.customer.phone_number) &
            Q(valid_date__gte=date.today())
        ).order_by('valid_date', 'credit')

        # 크레딧 점검
        total_credit = 0
        for credit in credit_list:
            total_credit += credit.credit
        if total_credit < booking.program.price:
            return Response({'message': '크레딧을 구매해주세요.', '현재 크레딧': total_credit}, status=status.HTTP_400_BAD_REQUEST)

        data = {'booking': booking_id}
        total_amount = booking.program.price
        for credit in credit_list:
            if total_amount > credit.credit:
                amount = credit.credit
            else:
                amount = total_amount
            total_amount -= amount
            credit.credit -= amount
            credit.save()
            data['credit'] = credit.id
            data['amount'] = amount
            serializer = PaymentCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if total_amount == 0:
                break

        booking.status = Booking.PAID
        booking.save()
        return Response({'message': '예약이 완료되었습니다.'}, status=status.HTTP_201_CREATED)


class BookingUpdateAPIView(UpdateAPIView):
    queryset = Booking
    serializer_class = BookingUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    # PATCH method
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.status != Booking.PAID:
            return Response({'message': '이미 환불되었거나, 아직 결제되지 않은 예약입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        date = instance.program.date
        if date - date.today() > timedelta(2):
            refund_rate = Decimal(1)
        elif date - date.today() > timedelta(0):
            refund_rate = Decimal(0.5)
        else:
            return Response({'message': '수업 당일부턴 예약을 취소할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        for payment in instance.payment_set.all():
            credit = payment.credit
            payment_data = {'refund_rate': refund_rate}
            payment_serializer = PaymentUpdateSerializer(instance=payment, data=payment_data)
            payment_serializer.is_valid(raise_exception=True)
            payment_serializer.save()
            credit.credit += refund_rate * payment.amount
            credit.save()

        data = {'status': Booking.REFUNDED}
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
