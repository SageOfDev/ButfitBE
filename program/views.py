from rest_framework.generics import CreateAPIView

from program.models import Program
from program.serializers import ProgramCreateSerializer


class ProgramCreateAPIView(CreateAPIView):
    queryset = Program
    serializer_class = ProgramCreateSerializer
