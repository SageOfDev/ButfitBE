# README
***
헬스클럽에서 수업의 생성과 쿠폰 머니의 충전, 이를 이용한 수업 예약을 구현한 프로젝트입니다.
해당 헬스클럽의 과제로 시작한 프로젝트입니다.

## 본론
***
### API url
#### program
- `/api/program/` (수업 셋팅)
#### mypage
- `/api/mypage/join/` (회원가입)
- `/api/mypage/login/` (로그인)
- `/api/mypage/logout/` (로그아웃)
- `/api/mypage/credit/`(크레딧 구매)

#### booking
- `api/booking/` (수업 예약)
- `api/booking/{int:pk}/` (수업 예약 취소)
#### admin
- (예약 현황 보기)
#### API docs url
- `/api/swagger/`


단계마다 설명과 함께 **테스트 데이터**가 있습니다. postman의 example로도 작성해두었으며, 순서대로 따라해주시면 제가 만든 모든 기능을 보실 수 있습니다.

### 1. 수업 셋팅하기
- method: `POST`
- url: `program/`
- 결과: 수업 셋팅

#### 요청 데이터
```
# 결제 과정, 예약 과정(정원, 중복), 환불 과정 테스트용 수업
{
    "location": "DG",
    "name": "상체",
    "price": 180000,
    "capacity": 1,
    "date": "2022-03-17",   # 테스트 당일로 지정해주십시오.
    "start_time": "10:00:00",
    "end_time": "11:00:00"
}
```
```
# 환불 과정 테스트용 수업 : 1일 후로 날짜 지정
{
    "location": "MD",
    "name": "하체",
    "price": 200000,
    "capacity": 4,
    "date": "2022-03-18",   # 테스트 당일로부터 1~2일 후로 지정해주십시오.
    "start_time": "10:00:00",
    "end_time": "11:00:00"
}
```
```
# 환불 과정 테스트용 수업 : 3일 후로 날짜 지정
{
    "location": "AGJ",
    "name": "복근",
    "price": 300000,
    "capacity": 4,
    "date": "2022-07-17",   # 테스트 당일로부터 3일~ 후로 지정해주십시오.
    "start_time": "10:00:00",
    "end_time": "11:00:00"
}
```
### 회원등록
인증 인가는 구현하지 못했습니다. 관리자 페이지 `Customers`(아래 url)에서 회원을 추가해주세요.
- url : `admin/mypage/customer/add/`
#### 관리자 페이지에서 회원 등록
```
# 예약과정(중복), 환불 과정(환불 불가) 테스트용 계정
{
    휴대폰 번호: 010-1111-1111
}
```
```
# 예약 과정(정원), 환불 과정(반액, 전액) 테스트용 계정
{
    휴대폰 번호: 010-2222-2222
}
```

### 2. 크레딧 구매하기
실제 거래가 이루어지는 부분이라 멱등성을 지닌 `PUT`메서드를 사용해 중복 결제를 방지하고자 하였습니다.
1) 크레딧 생성
- method: 'POST'
- url: 'mypage/credit/'
- 결과: 빈 크레딧 인스턴스가 생성되고, 2)의 url에 `GET`로 Redirect합니다.

2) 크레딧 및 사용기간 결정
- method: 'PUT'
- url: 'mypage/credit/<int:pk>/'
- 결과: 결제한 금액을 입력하면 정책에 따라 크레딧의 사용 가능 기간이 결정됩니다.

#### 요청 데이터
2) 의 GET 메서드를 구현하지 않아서 postman 보단 브라우저에서 url에 접속하셔서 DRF 템플릿에서 진행하시는 것을 추천드립니다.
```
# 1)의 url에서 진행해주십시오
{
    "customer": "010-1111-1111"
}
# 2)의 url에서 진행해주십시오
{
    "credit": 80000,
    "valid_date": null
}
```
```
# 1)
{
    "customer": "010-1111-1111"
}
# 2)
{
    "credit": 110000,
    "valid_date": null
}
```
```
# 1)
{
    "customer": "010-2222-2222"
}
# 2)
{
    "credit": 200000,
    "valid_date": null
}
```
```
# 1)
{
    "customer": "010-2222-2222"
}
# 2)
{
    "credit": 300000,
    "valid_date": null
}
```

### 3. 수업 예약 하기
1) 예약 생성
- method: `POST`
- url: `booking/`
- 결과: 아래 조건을 만족 시킬 때'결제 대기' 상태의 `Booking` 인스턴스가 생성되고, Redirect로 2) 과정을 실행합니다.
  - 중복 예약은 불가합니다.
  - 현재 결제 완료된 예약이 정원 미만이어야 합니다.
  
2) 예약 결제 정보 생성
- method: `POST`
- url: `booking/<int:booking_id>/payment/`
- 결과: 아래 순서로 결제를 진행하고, 완료 후엔 `Booking` 인스턴스의 `status`가 '결제 완료'로 수정됩니다.
  - 회원의 사용가능한 크레딧의 총합이 수업의 가격보다 많아야 합니다.
  - 사용 가능 기간이 이른 순(1순위), 크레딧의 값이 적은 순(2순위)으로 크레딧을 차감합니다.

#### 요청 데이터
모두 1) 의 url에서 진행해주십시오
```
# 성공 테스트용 예약
{
    "program": 1,
    "customer": "010-1111-1111"
}
```
```
# 실패(중복) 테스트용 예약
{
    "program": 1,
    "customer": "010-1111-1111"
}
```
```
# 실패(크레딧 부족) 테스트용 예약
{
    "program": 2,
    "customer": "010-1111-1111"
}
```
```
# 실패(정원 초과) 테스트용 예약
{
    "program": 1,
    "customer": "010-2222-2222"
}
```
```
# 환불 테스트용 예약
{
    "program": 2,
    "customer": "010-2222-2222"
}
```
```
# 환불 테스트용 예약
{
    "program": 3,
    "customer": "010-2222-2222"
}
```

### 4. 수업 예약 취소 하기
- method: `PATCH`
- url: `booking/<int:pk>/`
- 결과: 정책에 따라 'Payment' 인스턴스의 `refund_rate`가 update되고 `Booking` 인스턴스의 `status`가 `환불완료`로 수정됩니다.

#### 요청 데이터
```
# 환불 실패(수업 당일) 테스트용 
PATCH /booking/1/

# 환불 실패(미결제 예약) 테스트용 
PATCH /booking/2/

# 환불 성공(반액) 테스트용
PATCH /booking/3/

# 환불 실패(중복) 테스트용
PATCH /booking/3/

# 환불 성공(전액) 테스트용
PATCH /booking/4/
```
### 5. 수업 예약 리스트 보기
구현하지 못했습니다.

### 6. 수업 예약 현황 보기
1)
- url: `admin/booking/booking/`
- 결과: `list_filter`에서 특정 기간, 프로그램, 예약 상태를 필터링 할 수 있습니다.
- 라이브러리 : `rangefilter`

2)
- url: `admin/booking/booking/<ing:booking_id>/change/`
- 결과 : 예약에 사용된 `Payment`들 중 `refund_rate`가 `null`인 인스턴스를 확인함으로써 수업의 크레잇 차감 금액을 예약 내역 별로 볼 수 있습니다.
