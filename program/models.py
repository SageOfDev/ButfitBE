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
    location = models.CharField(max_length=3, choices=LOCATION_CHOICES)
    name = models.CharField(max_length=15)
    price = models.PositiveIntegerField()
    capacity = models.PositiveSmallIntegerField()
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
