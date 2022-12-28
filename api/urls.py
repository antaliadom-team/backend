from django.urls import path, include
from rest_framework.routers import DefaultRouter


from api.views.user_views import token, create_user, profile, MyDjoserViewSet
router = DefaultRouter()
router.register(r'users', MyDjoserViewSet)

app_name = 'api'

urlpatterns = [
    path('users/registration/', create_user, name='registration'),
    path('users/profile/', profile, name='profile'),
    path('users/token/', token, name='token'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
