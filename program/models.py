from django.db import models


class Program(models.Model):
    YEOKSAM = 'YS'
    DOGOK = 'DG'
    APGUJEONG = 'AGJ'
    MOKDONG = 'MD'
    JONGGAK = 'JG'
    LOCATION_CHOICES = [
        (YEOKSAM, '역삼'),
        (DOGOK, '도곡'),
        (APGUJEONG, '압구정'),
        (MOKDONG, '목동'),
        (JONGGAK, '종각'),
    ]
    location = models.CharField(max_length=3, choices=LOCATION_CHOICES, verbose_name='장소')
    name = models.CharField(max_length=15, verbose_name='수업 종류')
    price = models.PositiveIntegerField(verbose_name='수업 가격')
    capacity = models.PositiveSmallIntegerField(verbose_name='수업 정원')
    date = models.DateField(verbose_name='수업 날짜')
    start_time = models.TimeField(verbose_name='수업 시작 시간')
    end_time = models.TimeField(verbose_name='수업 종료 시간')
