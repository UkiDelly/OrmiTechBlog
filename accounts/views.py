# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from accounts.forms import UserCreationForm


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "accounts/user_create_form.html"


class UserLoginView(LoginView):
    template_name = "accounts/user_login_form.html"
    next_page = "/"


class UserLogoutView(LogoutView):
    next_page = "/"
