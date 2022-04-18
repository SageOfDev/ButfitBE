from datetime import date, timedelta

from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta

from mypage.models import Credit
from mypage.permissions import IsOwner
from mypage.serializers import CreditCreateSerializer, CreditUpdateSerializer, UserCreateSerializer, \
    UserLoginSerializer, TokenSerializer


class UserCreateAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            data=TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )


class UserLogoutAPIView(GenericAPIView):
    qeuryset = Token.objects.all()
    serializers_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serialzer = self.get_serializer(data=request.data)


class CreditCreateAPIView(CreateAPIView):
    queryset = Credit
    serializer_class = CreditCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = {'Location': 'http://127.0.0.1:8000/mypage/credit/%s/' % serializer.data['id']}
        return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreditUpdateAPIView(UpdateAPIView):
    queryset = Credit
    serializer_class = CreditUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    # PUT method
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        credit = request.data.get('credit', None)
        # INVALID_ERROR: 크레딧 구매시 1원 이상부터 가능하게 함.
        if credit in {None, 0}:
            return Response({'message': '1원 이상의 credit을 입력하십시오.'}, status.HTTP_400_BAD_REQUEST)

        months = credit // 100000 + 1
        valid_date = date.today() - timedelta(days=1) + relativedelta(months=months)
        data = {
            'credit': credit,
            'valid_date': valid_date
        }

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)