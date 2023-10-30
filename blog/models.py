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

    def get_upload_to(self, filename):
        return f"blog/{self.pk}/{filename}"

    thumbnail = models.ImageField(upload_to=get_upload_to, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    view_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name="blog_like")
    categorys = models.ManyToManyField(
        "Category", blank=True, related_name="blog_category"
    )

    class Meta:
        db_table = "blog"

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name
