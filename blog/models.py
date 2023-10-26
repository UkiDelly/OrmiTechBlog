from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from accounts.models import User


# Create your models here.
class BaseDateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(BaseDateTime):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    tags = models.CharField(max_length=100, blank=True)
    view_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name="blog_like")

    class Meta:
        db_table = "blog"


class Comment(BaseDateTime):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.content
