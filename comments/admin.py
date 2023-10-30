from django.contrib import admin

from comments.forms import CommentForm, ReCommentForm
from comments.models import Comment, ReComment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentForm
    list_display = ["content", "author", "created_at"]
    fields = ["content", "author", "blog"]


@admin.register(ReComment)
class ReCommentAdmin(admin.ModelAdmin):
    form = ReCommentForm
    list_display = ["content", "author", "created_at"]
    fields = ["comment", "content", "author"]
