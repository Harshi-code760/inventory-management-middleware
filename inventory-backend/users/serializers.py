# from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework import serializers

class Register(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio')
        read_only_fields = ('id', 'username')
    