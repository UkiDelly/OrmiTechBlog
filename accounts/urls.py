from django.urls import path

from accounts.views import UserRegisterView, UserLoginView

app_name = "accounts"
urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLoginView.as_view(), name="logout"),
]
