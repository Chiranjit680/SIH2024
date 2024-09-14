from django.urls import path,include
from .views import RegisterView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    
    path('login/',obtain_auth_token,name='login' ),
   path('register/', RegisterView.as_view(), name='register'),
    
]