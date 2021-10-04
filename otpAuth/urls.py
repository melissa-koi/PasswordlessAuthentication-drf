from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify_magiclink/',views.VerifyMagicLink.as_view(), name='magiclink-verify'),
    path('verify_otp/', views.VerifyOTP.as_view(), name='otp-verify')
]