from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserCreationForm, UserChangeForm
from accounts.models import User


# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("name", "username", "email", "is_admin")
    list_filter = ("is_admin",)

    # 관리 페이지에서 나타나게 할 목록을 보여줍니다.
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "name",
                    "nickname",
                    "email",
                    "description",
                    "profile_image",
                )
            },
        ),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    # 새로운 유저를 추가할때
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "username",
                    "email",
                    "nickname",
                    "description",
                    "profile_image",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.unregister(Group)
