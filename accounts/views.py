# Create your views here.
from django.views.generic import CreateView

from accounts.forms import UserCreationForm


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "accounts/user_create_form.html"
