# README
## admin 계정
id: admin
password: admin


## 과제 설명
### 1. 수업 셋팅하기
method: `POST`
url: `program/`
결과: 수업 셋팅

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

#### 크레딧 구매하기
실제 거래가 이루어지는 부분이라 멱등성을 지닌 `PUT`메서드를 사용해 중복 결제를 방지하고자 하였습니다.
1)
method: 'POST'
url: 'mypage/credit/'
결과: 빈 크레딧 인스턴스가 생성됩니다.

> 요청 데이터
```
{
    "customer": "010-1234-1234"
}
```

2)
method: 'PUT'
url: 'mypage/credit/<int:pk>'
결과: 결제한 금액을 입력하면 정책에 따라 크레딧의 사용 가능 기간이 결정됩니다.

> 요청 데이터
```
{
    "credit": 50000,
    "valid_date": null
}
```

