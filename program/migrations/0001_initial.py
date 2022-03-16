# Generated by Django 4.0.3 on 2022-03-16 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('YS', '역삼'), ('DG', '도곡'), ('AGJ', '압구정'), ('MD', '목동'), ('JG', '종각')], max_length=3, verbose_name='장소')),
                ('name', models.CharField(max_length=15, verbose_name='수업 종류')),
                ('price', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='수업 가격')),
                ('capacity', models.PositiveSmallIntegerField(verbose_name='수업 정원')),
                ('date', models.DateField(verbose_name='수업 날짜')),
                ('start_time', models.TimeField(verbose_name='수업 시작 시간')),
                ('end_time', models.TimeField(verbose_name='수업 종료 시간')),
            ],
        ),
    ]
