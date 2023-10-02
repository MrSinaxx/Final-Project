from django.urls import path
from .views import *



urlpatterns = [
    path('api/signup', RegistrationAPIView.as_view(), name='signup'),
    path('api/login', LoginAPIView.as_view(), name='login'),
    path('api/logout', LogOutAPIView.as_view(), name='logout'),
    path('api/user', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('api/changepass', ChangePasswordView.as_view(), name='change_password'),
    path('api/refresh', RefreshTokenAPIView.as_view(), name='refresh'),
    path('api/access', AccessTokenAPIView.as_view(), name='access'),
]