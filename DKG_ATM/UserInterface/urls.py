"""
URL configuration for DKG_ATM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("send-login-otp/", views.send_login_otp, name="send_login_otp"),
    path("logout/", views.logout_view, name="logout"),
    path('next_page/', views.next_page, name="next_page"),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('verify-otp/', views.verify_otp, name="verify_otp"),
    path('reset-password/', views.reset_password, name="reset_password"),
]

