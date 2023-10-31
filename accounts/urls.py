from django.contrib.auth.decorators import login_required
from django.urls import path

from accounts.views import (
    UserRegisterView,
    UserLoginView,
    get_token,
    UserLogoutView,
    UserInfoView,
    UserInfoUpdateView,
)

app_name = "accounts"
urlpatterns = [
    path("myinfo/", UserInfoView.as_view(), name="my_info"),
    path("myinfo/update/", UserInfoUpdateView.as_view(), name="my_info_update"),
    path("signup/", UserRegisterView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("token/", login_required(get_token), name="get_token"),
]
