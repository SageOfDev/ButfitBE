from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from booking.models import Booking
from mypage.models import Credit


class CreditCreateSerializer(ModelSerializer):
    credit = serializers.IntegerField(label='크레딧(원)', read_only=True)
    valid_date = serializers.DateField(label='사용 가능 기간', read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    # TODO 인가 기능 추가시 아래 코드 활성화, 수정 필요할 수 있음.
    # customer = serializers.PrimaryKeyRelatedField(label='고객', queryset=Customer.objects.all(), read_only=True)

    class Meta:
        model = Credit
        fields = '__all__'


class CreditUpdateSerializer(ModelSerializer):
    class Meta:
        model = Credit
        fields = ['credit', 'valid_date']


class UserSerializer(ModelSerializer):
    credits = serializers.PrimaryKeyRelatedField(many=True, queryset=Credit.objects.all())
    booking = serializers.PrimaryKeyRelatedField(many=True, queryset=Booking.objects.all())

    class Meta:
        Model = User
        fields = ['id', 'username', 'credits', 'bookings']