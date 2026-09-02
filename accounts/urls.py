from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts import views as account

urlpatterns = [
    path("login/", account.SignIn.as_view(), name="login"),
    path("register/", account.Register.as_view(), name="register"),
    path("profile/", account.ProfileUpdateView.as_view(), name="profile"),
    path("logout/", login_required(LogoutView.as_view()), name="logout"),
]
