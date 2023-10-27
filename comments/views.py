import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound
from django.views import View

from blog.models import Blog
from comments.models import Comment


# Create your views here.
def comment_list(request: HttpRequest, **kwargs):
    blog = Blog.objects.get(pk=kwargs["pk"])
    comments = blog.comment_set.all().order_by("-created_at")
    comments = [comment.toJson() for comment in comments]
    return JsonResponse(comments, status=200, safe=False)


class AddComment(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest, **kwargs):
        body: dict = json.loads(request.body)
        blog = Blog.objects.get(pk=kwargs["pk"])

        if blog is None:
            return HttpResponseNotFound()
        comment = Comment.objects.create(
            content=body.get("content"),
            author=request.user,
            blog=Blog.objects.get(pk=kwargs["pk"]),
        )

        return JsonResponse(comment.toJson(), status=200)
