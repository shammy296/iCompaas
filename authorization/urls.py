from django.urls import path
from knox import views as knox

from authorization.views import UserInfoView, RegisterView, ResetPasswordView, LoginView

urlpatterns = [
    path('user/', UserInfoView.as_view()),
    path('user/<int:pk>/', UserInfoView.as_view()),
    path('register/', RegisterView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox.LogoutView.as_view(), name='knox_logout'),
]
