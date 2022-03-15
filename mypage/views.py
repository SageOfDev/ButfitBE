from datetime import date, timedelta

from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta

from mypage.models import Credit
from mypage.serializers import CreditCreateSerializer, CreditUpdateSerializer


class CreditCreateAPIView(CreateAPIView):
    queryset = Credit
    serializer_class = CreditCreateSerializer


class CreditUpdateAPIView(UpdateAPIView):
    queryset = Credit
    serializer_class = CreditUpdateSerializer

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