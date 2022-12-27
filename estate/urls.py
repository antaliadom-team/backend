from django.urls import path, include
from rest_framework import routers
from .views import FlatViewSet

router = routers.DefaultRouter()
router.register(r'estate', FlatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]