import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from booking.models import Booking
from mypage.models import Credit


class UserCreateSerializer(ModelSerializer):
    username = serializers.CharField(help_text="'-'를 포함한 번호를 입력해주세요.", validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', "confirm_password", 'date_joined']

    def validate_username(self, value):
        p = re.compile(r'010-\d{4}-\d{4}')
        if p.match(value) is None:
            raise serializers.ValidationError("잘못된 핸드폰 번호 양식입니다.")
        return value

    def validate(self, data):
        if data.get('password', None) != data.get('confirm_password', ''):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        del data['confirm_password']
        data['password'] = make_password(data['password'])
        return data


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