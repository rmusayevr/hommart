from django.urls import path
from .views import (
    RegisterView, 
    CustomLoginView, 
    ProfileView, 
    ProfileMobileView,
    ContactView, 
    ForgetPasswordView,
    ResetPasswordView,
    SuccessResetPasswordView,
    SuccessForgetPasswordView,
    myorders, 
    activate)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('confirmation/<str:uidb64>/<str:token>/', activate, name='confirmation'),
    path('register/', RegisterView.as_view(), name = "register"),
    path('login/', CustomLoginView.as_view(), name = "login"),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('forget_password/success/',
        SuccessForgetPasswordView.as_view(), name="success_forget_password"),
    path('reset_password/<str:uidb64>/<str:token>/',
        ResetPasswordView.as_view(), name="reset_password"),
    path('reset_password/success/',
        SuccessResetPasswordView.as_view(), name="success_reset_password"),
    path('profile/<int:pk>/', ProfileView.as_view(), name = "profile"),
    path('profile_mobile/', ProfileMobileView.as_view(), name = "profile_mobile"),
    path('contact/<int:pk>/', ContactView.as_view(), name = "contact"),
    path('myorders/', myorders, name = "myorders"),

]