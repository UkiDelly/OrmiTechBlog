from django.contrib import admin

from blog.forms import BlogForm
from blog.models import Blog


# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    list_display = ["title", "author", "created_at"]
