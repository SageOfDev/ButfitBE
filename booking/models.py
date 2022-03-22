from django.db import models


class Booking(models.Model):
    PAID = 'P'
    REQUIRED_TO_PAY = 'RTP'
    REFUNDED = 'RF'
    STATUS_CHOICES = [
        (PAID, '결제 완료'),
        (REQUIRED_TO_PAY, '결제 대기'),
        (REFUNDED, '환불 완료'),
    ]

    program = models.ForeignKey('program.Program', null=True, on_delete=models.SET_NULL, verbose_name='수업 번호')
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=REQUIRED_TO_PAY, verbose_name='결제 상태')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='회원 휴대폰 번호')

    created_dt = models.DateTimeField(auto_now_add=True, verbose_name='예약 생성 시각')
    modified_dt = models.DateTimeField(auto_now=True, verbose_name='예약 상태 변경 시각')


# 결제 정보
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name='예약 번호')
    credit = models.ForeignKey('mypage.Credit', null=True, on_delete=models.SET_NULL, verbose_name='사용된 크레딧 번호')
    amount = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='결제 금액(원)')
    refund_rate = models.DecimalField(max_digits=4, decimal_places=3, null=True, default=None, verbose_name='환불 정책률')

    created_dt = models.DateTimeField(auto_now_add=True, verbose_name='결제 시각')
    modified_dt = models.DateTimeField(auto_now=True, verbose_name='결제 정보 변경 시각')