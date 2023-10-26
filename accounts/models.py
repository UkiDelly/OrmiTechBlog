from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
        self, name, username, email, password, description, nickname, profile_image=None
    ):
        if not username:
            raise ValueError("아이디를 입력해주세요")
        if not email:
            raise ValueError("이메일을 입력해주세요")

        user = self.model(
            name=name,
            username=username,
            email=self.normalize_email(email),
            nickname=nickname,
            description=description,
            created_at=datetime.now(),
            profile_image=profile_image,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, username, nickname, email, password):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            username=username,
            nickname=nickname,
            description="",
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100, default=None, blank=True)
    description = models.TextField(default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def get_upload_to(self, filename):
        return f"profile/{self.username}/{filename}"

    profile_image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
        "name",
        "nickname",
    ]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
