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
    fieldsets = (
        ("Personal info", {"fields": ("name", "email")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     list_display = ('name','email','address','phone_number','is_admin')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (None,{'fields':('name','email','password')}),
#         ("Personal info",{'fields':('address','phone_number')}),
#         ("Permissions",{'fields':('is_admin',)})
#     )
#
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('name','email', 'address','phone_number', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()
#

admin.site.unregister(Group)
