from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from .helpers import create_otp
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views, permissions

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data = request.data)

            if not serializer.is_valid():
                return Response({
                    'status': 403,
                    'errors': serializer.errors
                })
            serializer.save()

            # TOKEN
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('magiclink-verify')

            absurl = 'http://' +  current_site + relativeLink + "?otp=" + user.otp + "&email=" + str(user.email)
            email_body = 'Hi, Your OTP is: ' + user.otp + ' or you can use the link below to verify your email. \n' + absurl
            data = {'email_subject': 'Verify your email', 'email_body': email_body, 'to_email': user.email}
            Util.send_email(data)
            return Response({
                'status': 201,
                'message': 'an otp sent to your number and email'},
                status=status.HTTP_201_CREATED)

        # return Response({
        #         'status': 200,
        #         'message': 'an otp sent on your number and email'
        #     })

        except Exception as e:
            print('Exception here')
            print(e)

        return Response({
            'status': 404,
            'error': 'something went wrong'
        })


class VerifyOTP(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        email = request.data.get('email', False)
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)
        print(email, phone, otp_sent)

        if phone and email and otp_sent:
            user = User.objects.filter(email__iexact=email)
            if user.exists():
                user = user.first()
                otp= user.otp
                print(str(otp))
                if str(otp_sent) == str(otp):
                    user.is_email_verified = True
                    user.save()
                    return Response({
                        'status' : True,
                        'detail' : 'OTP matched. Please proceed to login.'
                    })

                else:
                    return Response({
                        'status' : False,
                        'detail' : 'OTP incorrect.'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'No user Found. Register to login.'
                })
        else:
            return Response({
                'status' : False,
                'detail' : 'Please provide email, phone and otp for validations'
            })


class VerifyMagicLink(APIView):
    def get(self, request):
        try:
            otp = request.GET.get('otp')
            email = request.GET.get('email')

            print(email, otp)
            if otp and email:
                user = User.objects.get(otp=otp)
                user.is_email_verified = True
                user.save()
                print(user)
            else:
                return Response({
                    'status' : False,
                    'detail' : 'No user Found. Register to login.'
                })

            return Response({
                'status' : True,
                'detail' : 'OTP matched. Please proceed to login.'
            })

        except:
            return Response({
                'status' : False,
                'detail' : 'Otp not verified'
            })



