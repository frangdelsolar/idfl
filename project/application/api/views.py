from rest_framework import viewsets

from application.api.serializers import ApplicationSerializer
from application.models import Application

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer