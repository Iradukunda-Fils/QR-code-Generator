from django.urls import path
from .views import (CustomLoginView, UserRegistrationView, LogoutView,
                   DownloadQRCodeView, AdminView, UsersView, UserUpdateView)

#PASSWORD RESET PROCESSIES
from django.urls import path
from .views import ( DetailsView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', AdminView.as_view(), name='home-admin'),
    path('user/', UsersView.as_view(), name='user-qr'),
]

#PASSWORD RESET PROCESSIES

urlpatterns += [
    path('password-reset/done/', 
         CustomPasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('password-reset/complete/', 
         CustomPasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
]


#USER PROFILES
urlpatterns +=[
    path('user-details/<int:id>', DetailsView.as_view(), name='user-detail'),
    path('user-details/update/<int:pk>', UserUpdateView.as_view(), name='user-update'),
]


#DOWNLOAD QR CODE



urlpatterns += [
    path('download-qr/<int:user_id>/', DownloadQRCodeView.as_view(), name='download_qr_code'),
]