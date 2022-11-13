from django.urls import path
from .views import UserDetailsListAPIView, LoginViewSet, RefreshViewSet, RegisterReferralView, Invite, RegisterView, LoginView2, LogoutAPIView, LoadUserView, SetNewPasswordAPIView, VerifyEmail, LoginAPIView, PasswordTokenCheckAPI, RequestPasswordResetEmail
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('register/referral/', RegisterReferralView.as_view(),
         name="register-referral"),
    path('login2/', LoginViewSet, name='auth-login'),
    path('refresh/', RefreshViewSet, name='auth-refresh'),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('invite/', Invite.as_view(), name="get-referral"),
    path('sign-in/', LoginView2.as_view(), name="sign-in"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('loaduser/', LoadUserView.as_view(), name="load-user"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('list-users/', UserDetailsListAPIView.as_view(), name="user-details"),

]
