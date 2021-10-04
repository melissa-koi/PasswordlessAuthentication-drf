from rest_framework import serializers
from .models import User
from .helpers import create_otp
from django.contrib import auth

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'phone']

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], phone=validated_data['phone'])
        user.save()
        create_otp(user.phone, user)
        user.save_twilio()
        return user


