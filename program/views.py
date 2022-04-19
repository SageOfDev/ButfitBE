from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from program.models import Program
from program.permissions import IsSuperUser
from program.serializers import ProgramCreateSerializer


class ProgramCreateAPIView(CreateAPIView):
    queryset = Program
    serializer_class = ProgramCreateSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
