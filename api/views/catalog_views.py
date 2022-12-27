from rest_framework import viewsets
from .models import Object, User
from .serializers import EstateSerializer


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = EstateSerializer
