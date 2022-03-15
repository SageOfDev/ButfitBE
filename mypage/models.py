from django.db import models


class Customer(models.Model):
    phone_number = models.CharField(primary_key=True, max_length=13, verbose_name='휴대폰 번호')
    created_d = models.DateField(auto_now_add=True, verbose_name='등록 날짜')
    modified_d = models.DateField(auto_now=True, verbose_name='정보 변경 날짜')


class Credit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='고객')
    credit = models.PositiveIntegerField(verbose_name='크레딧(원)', null=True)
    valid_date = models.DateField(verbose_name='사용 가능 기간', null=True)

    created_d = models.DateField(auto_now_add=True, verbose_name='생성 날짜')
    modified_d = models.DateField(auto_now=True, verbose_name='수정 날짜')