from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('api/', include('api.v1.urls')),
    
]
