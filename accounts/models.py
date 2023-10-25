from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, username, email, password):
        if not name:
            raise ValueError("must have user email")
        if not email:
            raise ValueError("must have user email")
        user = self.model(
            name=name,
            username=username,
            email=self.normalize_email(email),
            created_at=datetime.now(),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, username, email, password):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            username=username,
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
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
        "name",
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
