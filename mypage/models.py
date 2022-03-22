from django.db import models


class Credit(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='회원')
    credit = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='크레딧(원)', null=True)
    valid_date = models.DateField(verbose_name='사용 가능 기간', null=True)

    created_d = models.DateField(auto_now_add=True, verbose_name='생성 날짜')
    modified_d = models.DateField(auto_now=True, verbose_name='수정 날짜')
