from django.contrib.auth.decorators import login_required
from django.urls import path

from accounts.views import UserRegisterView, UserLoginView, get_token, UserLogoutView

app_name = "accounts"
urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("token/", login_required(get_token), name="get_token"),
]
