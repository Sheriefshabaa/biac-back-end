"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
# from .serializers import LoginTokenObtainPairSerializer
from django.urls import path
from .views import LoginView ,LogoutBlacklistTokenUpdateView



urlpatterns = [
    path(
        'registration/account-confirm-email/<str:key>/',
        ConfirmEmailView.as_view(),
    ),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path(
        'password/reset/confirm/<slug:uidb64>/<slug:token>/',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'
    ),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('login/', LoginView.as_view(), name='login'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutBlacklistTokenUpdateView.as_view(),name='blacklist'),
]
