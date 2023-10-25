from django import forms

from .models import User


class UserCreationForm(forms.ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput)
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    username = forms.CharField(label="Username", widget=forms.TextInput)
    description = forms.TextInput()
    profile_image = forms.ImageField(widget=forms.FileInput)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = "__all__"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput)
    name = forms.CharField(label="Name", widget=forms.TextInput)
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    description = forms.TextInput()
    profile_image = forms.ImageField(label="Profile Image")

    class Meta:
        model = User
        fields = ["name", "email", "description", "profile_image"]

    def clean_password(self):
        return self.initial["password"]
