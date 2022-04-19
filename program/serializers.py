from rest_framework.serializers import ModelSerializer

from program.models import Program


class ProgramCreateSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
