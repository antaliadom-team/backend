from django.urls import path, include
from rest_framework import routers
from .views import FlatViewSet, BuyViewSet, RentViewSet

router = routers.DefaultRouter()
router.register(r'flats', FlatViewSet)
router.register(r'buy', BuyViewSet)
router.register(r'rent', RentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
