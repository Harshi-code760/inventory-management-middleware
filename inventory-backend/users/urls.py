from django.urls import path
from .views import RegisterView, Profile, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', Profile.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name="password-reset"),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]