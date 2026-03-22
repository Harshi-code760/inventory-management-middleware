# from django.shortcuts import render
from rest_framework import generics, status
# from django.contrib.auth.models import User
from .serializers import Register , UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, PasswordReset
from django.contrib.auth.hashers import make_password
import secrets
from inventory.emails import send_password_reset

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = Register

class Profile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfile

    def get_object(self):
        return self.request.user
    
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            PasswordReset.objects.create(user=user, token=token)
            send_password_reset(email,token)
        except CustomUser.DoesNotExist:
            pass
        return Response(
            {"detail": "If that email exists, a reset link has been sent."},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(APIView):
    def post(self, request):
        token_str = request.data.get('token')
        new_password = request.data.get('password')

        if not token_str or not new_password:
            return Response(
                {"detail": "Token and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 8:
            return Response(
                {"detail": "Password must be at least 8 chars"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            reset_token = PasswordReset.objects.get(token=token_str)
        except PasswordReset.DoesNotExist:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not reset_token.is_valid():
            return Response(
                {"detail": "Token has expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reset_token.user.password = make_password(new_password)
        reset_token.user.save()
        reset_token.used = True
        reset_token.save()

        return Response(
            {"detail": "Password Reset"},
            status=status.HTTP_200_OK
        )