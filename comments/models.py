from django.db import models

from accounts.models import User
from blog.models import BaseDateTime, Blog


# Create your models here.
class Comment(BaseDateTime):
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        db_table = "comment"

    def __str__(self):
        return f'{self.content}'

    def toJson(self):
        return {
            "id": self.pk,
            "content": self.content,
            "author": self.author.toJson(),
            "blog": self.blog.pk,
            "reply": [comment.toJson() for comment in self.reply.all()],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ReComment(BaseDateTime):
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=False)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="reply")

    class Meta:
        db_table = "recomment"

    def __str__(self):
        return f'{self.content}'

    def toJson(self):
        return {
            "id": self.pk,
            "parent_comment": self.comment.pk,
            "content": self.content,
            "author": self.author.toJson(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
