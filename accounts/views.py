# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, JsonResponse
from django.middleware import csrf
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from accounts.forms import UserCreationForm
from accounts.models import User


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "accounts/user_create_form.html"


class UserLoginView(LoginView):
    template_name = "accounts/user_login_form.html"
    next_page = "/"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("blog:blog_list")


class UserInfoView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/my_info.html"

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = {"user": user.toJson()}
        return context


def get_token(request: HttpRequest):
    token = csrf.get_token(request)
    return JsonResponse({"token": token}, status=200)
