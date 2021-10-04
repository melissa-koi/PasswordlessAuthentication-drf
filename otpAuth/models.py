from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import message, send_mail
import uuid
from django.conf import settings
from twilio.rest import Client
from decouple import config
import os
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=9)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=200, null=True, blank=True)
    otp = models.CharField(max_length=6,null=True)
    forget_password_token = models.CharField(max_length=200, null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def name(self):
        return self.first_name + ' ' + self.last_name

    def name2(self):
        return self.phone

    def save_twilio(self, *args, **kwargs):
        if self.otp:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=f'Your OTP is: {self.otp}',
                from_='+12704798201',
                to=f'+254{self.phone}'
            )

            print(message.sid)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return self.email

# @receiver(post_save, sender=User)
# def send_email_token(sender, instance, created, **kwargs):
#     if created:
#         try:
#             subject = "Your email needs to be verified"
#             message = f'Hi, click on the link to verify email http://127.0.0.1:8000/{uuid.uuid4()}/'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [instance.email]
#
#             send_mail(subject , message , email_from , recipient_list)
#         except Exception as e:
#             print(e)
#
#
