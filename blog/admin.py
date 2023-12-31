from django.contrib import admin

from blog.forms import BlogForm, CategoryForm
from blog.models import Blog, Category


# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    list_display = ["title", "author", "created_at"]
    fields = [
        "title",
        "thumbnail",
        "content",
        "author",
        "view_count",
        "likes",
        "categorys",
    ]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ["name"]
    fields = ["name"]
