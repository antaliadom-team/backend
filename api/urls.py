from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.user_views import MyDjoserViewSet, token, MyTokenObtainPairView

router = DefaultRouter()
router.register(r'users', MyDjoserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/token/', token, name='token')
    # path('auth/token/', MyTokenObtainPairView.as_view(), name='token'),
]
