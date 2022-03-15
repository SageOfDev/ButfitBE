from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from booking.models import Booking, Payment
from program.models import Program


class BookingCreateSerializer(ModelSerializer):
    status = serializers.ChoiceField(choices=[('P', '결제 완료'), ('RTP', '결제 대기'), ('RF', '환불 완료')], label='결제 상태', read_only=True)

    # 예약 생성시 null은 불가. 반드시 원하는 수업 선택해야함.
    program = serializers.PrimaryKeyRelatedField(allow_null=False, label='수업 번호', queryset=Program.objects.all())

    # 인가기능 구현시 아래코드 수정 필요
    # customer = serializers.PrimaryKeyRelatedField(label='회원 휴대폰 번호', queryset=Customer.objects.all())

    class Meta:
        model = Booking
        fields = '__all__'


class PaymentCreateSerializer(ModelSerializer):
    refund_ratio = serializers.FloatField(allow_null=True, label='환불 정책 비율', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class BookingUpdateSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']


class PaymentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['refund_rate', 'modified_dt']