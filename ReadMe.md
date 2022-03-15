# README
***

## admin 계정
- id: admin
- password: admin


## 과제 설명
### 1. 수업 셋팅하기
- method: `POST`
- url: `program/`
- 결과: 수업 셋팅

> 요청 데이터
```
{
    "location": "YS",
    "name": "상체",
    "price": 130000,
    "capacity": 3,
    "date": "2022-03-17",
    "start_time": "10:00:00",
    "end_time": "11:00:00"
}
```


### 2. 크레딧 구매하기
#### 인증 및 인가 기능
구현하지 못하여서, 관리자 페이지, `Customers`에서 직접 회원을 등록해야 합니다.

> 요청 데이터
```
{
    "phone_number": "010-1234-1234"
}
```

#### 크레딧 구매
실제 거래가 이루어지는 부분이라 멱등성을 지닌 `PUT`메서드를 사용해 중복 결제를 방지하고자 하였습니다.
1) 크레딧 생성
- method: 'POST'
- url: 'mypage/credit/'
- 결과: 빈 크레딧 인스턴스가 생성되고, 2)의 url에 `GET`로 Redirect합니다.

> 요청 데이터
```
{
    "customer": "010-1234-1234"
}
```

2) 크레딧 및 사용기간 결정
- method: 'PUT'
- url: 'mypage/credit/<int:pk>'
- 결과: 결제한 금액을 입력하면 정책에 따라 크레딧의 사용 가능 기간이 결정됩니다.

> 요청 데이터
```
{
    "credit": 50000,
    "valid_date": null
}
```

### 3. 수업 예약 하기
1) 예약 생성
- method: 'POST'
- url: 'booking/'
- 결과: 아래 조건을 만족 시킬 때'결제 대기' 상태의 `Booking` 인스턴스가 생성되고, Redirect로 2) 과정을 실행합니다.
  - 중복 예약은 불가합니다.
  - 현재 결제 완료된 예약이 정원 미만이어야 합니다.

> 요청 데이터
```
{
    "program": 1,
    "customer": "010-1234-1234"
}
```
-
2) 예약 결제 정보 생성
- method: 'POST'
- url: 'booking/<int:booking_id>/payment/'
- 결과: 아래 순서로 결제를 진행하고, 완료 후엔 `Booking` 인스턴스의 `status`가 '결제 완료'로 수정됩니다.
  - 회원의 사용가능한 크레딧의 총합이 수업의 가격보다 많아야 합니다.
  - 사용 가능 기간이 이른 순(1순위), 크레딧의 값이 적은 순(2순위)으로 크레딧을 차감합니다.

### 4. 수업 예약 취소 하기
- method: 'PATCH'
- url: 'booking/<int:pk>/'
- 결과: 정책에 따라 'Payment' 인스턴스의 `refund_rate`가 update되고 `Booking` 인스턴스의 `status`가 `환불완료`로 수정됩니다.