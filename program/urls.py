from django.urls import path

from program.views import ProgramCreateAPIView

urlpatterns = [
    path('', ProgramCreateAPIView.as_view(), name='program')
]