# from django.shortcuts import render
from rest_framework import generics
# from django.contrib.auth.models import User
from .serializers import Register , UserProfile
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
from .models import CustomUser

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = Register

class Profile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfile

    def get_object(self):
        return self.request.user