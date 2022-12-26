from rest_framework import viewsets
from .models import Estate, Buy, Rent, User
from .serializers import EstateSerializer, BuySerializer, RentSerializer


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer


class BuyViewSet(viewsets.ModelViewSet):
    queryset = Buy.objects.all()
    serializer_class = BuySerializer


class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
