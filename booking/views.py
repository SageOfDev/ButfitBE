from datetime import date

from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from booking.models import Booking, Payment
from booking.serializers import BookingCreateSerializer, PaymentCreateSerializer
from mypage.models import Customer, Credit
from program.models import Program


class BookingCreateAPIView(CreateAPIView):
    queryset = Booking
    serializer_class = BookingCreateSerializer

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
        headers = {'Location': 'http://127.0.0.1:8000/booking/%s/payment/' % serializer.data['id']}
        return Response(serializer.data, status=status.HTTP_307_TEMPORARY_REDIRECT, headers=headers)


class PaymentCreateAPIView(APIView):

    def post(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)

        credit_list = Credit.objects.filter(
            Q(customer__phone_number=booking.customer.phone_number) &
            Q(valid_date__gte=date.today())
        ).order_by('valid_date', 'credit')

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
                total_amount -= amount
            else:
                amount = total_amount
            credit.credit -= amount
            credit.save()

            data['amount'] = amount
            serializer = PaymentCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if total_amount == 0:
                break
        booking.status = Booking.PAID
        booking.save()
        return Response({'message': '예약이 완료되었습니다.'}, status=status.HTTP_201_CREATED)



