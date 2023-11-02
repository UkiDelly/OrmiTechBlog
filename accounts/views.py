# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.middleware import csrf
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from accounts.forms import UserCreationForm, UserChangeForm
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


class UserInfoView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "accounts/my_info.html"

    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        context = {"user": user.toJson()}
        return context


class UserInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    success_url = reverse_lazy("accounts:my_info")
    template_name = "accounts/user_change_form.html"

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(self.get_success_url())


def get_token(request: HttpRequest):
    token = csrf.get_token(request)
    return JsonResponse({"token": token}, status=200)
