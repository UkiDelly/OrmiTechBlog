from django import forms

from .models import User


class UserCreationForm(forms.ModelForm):
    name = forms.CharField(label="이름", widget=forms.TextInput)
    email = forms.EmailField(label="이메일", widget=forms.EmailInput)
    nickname = forms.CharField(label="별명", widget=forms.TextInput)
    username = forms.CharField(label="아이디", widget=forms.TextInput)
    description = forms.Textarea()
    profile_image = forms.ImageField(widget=forms.FileInput, required=False)
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "username",
            "nickname",
            "description",
            "profile_image",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        print(password1, password2)
        return password2

    def save(self, commit=True):
        user: User = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    name = forms.CharField(label="이름", widget=forms.TextInput)
    email = forms.EmailField(label="이메일", widget=forms.EmailInput)
    nickname = forms.CharField(label="별명", widget=forms.TextInput)
    description = forms.Textarea()
    profile_image = forms.ImageField(label="프로필 사진", widget=forms.FileInput, required=False, allow_empty_file=True)

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "nickname",
            "description",
            "profile_image",
        ]
