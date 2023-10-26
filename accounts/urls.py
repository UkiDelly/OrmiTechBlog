from django.urls import path

from accounts.views import UserRegisterView

urlpatterns = [path("signup/", UserRegisterView.as_view(), name="signup")]
