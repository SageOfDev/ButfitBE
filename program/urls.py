from django.urls import path

from program.views import ProgramCreateAPIView

app_name = "program"

urlpatterns = [
    path('', ProgramCreateAPIView.as_view(), name='list')
]