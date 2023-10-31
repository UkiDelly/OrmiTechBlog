import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound
from django.views import View

from blog.models import Blog
from comments.forms import CommentForm
from comments.models import Comment, ReComment


# Create your views here.
class CommentListView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, **kwargs):
        blog = Blog.objects.get(pk=kwargs["pk"])
        comments = blog.comment_set.all().order_by("-created_at")
        comments = [comment.toJson() for comment in comments]
        return JsonResponse(comments, status=200, safe=False)


class CommentView(LoginRequiredMixin, View):
    http_method_names = ["get", "post", "put", "delete"]

    def get(self, request: HttpRequest, **kwargs):
        comment = Comment.objects.get(pk=kwargs["comment_pk"])
        if comment is None:
            return HttpResponseNotFound()
        comment_form = CommentForm(instance=comment)
        return JsonResponse(comment_form, status=200, safe=False)

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

    def put(self, request: HttpRequest, **kwargs):
        body: dict = json.loads(request.body)
        comment = Comment.objects.get(pk=kwargs["pk"])

        if comment is None:
            return HttpResponseNotFound()
        comment.content = body.get("content")
        comment.save()
        return JsonResponse(comment.toJson(), status=200)

    def delete(self, request: HttpRequest, **kwargs):
        comment = Comment.objects.get(pk=kwargs["pk"])
        if comment is None:
            return HttpResponseNotFound()
        comment.delete()
        return JsonResponse(True, status=200, safe=False)


class ReplyCommentView(LoginRequiredMixin, View):
    http_method_names = ["post", "put", "delete"]

    def post(self, request: HttpRequest, **kwargs):
        print(kwargs)
        print(json.loads(request.body))
        return JsonResponse(True, status=200, safe=False)
        # parent_comment_id = kwargs.get("pk")
        # body: dict = json.loads(request.body)
        # ReComment.objects.create(
        #     content=body.get("content"),
        #     author=request.user,
        #     comment=Comment.objects.get(pk=parent_comment_id),
        # )
        #
        # if parent_comment_id is None:
        #     return HttpResponseNotFound()

    def put(self, request: HttpRequest, **kwargs):
        pk = kwargs.get("reply_pk")
        body: dict = json.loads(request.body)
        reply = ReComment.objects.get(pk=pk)

        if reply:
            reply.content = body.get("content")
            reply.save()
            return JsonResponse(reply.toJson(), status=200)
        return HttpResponseNotFound()

    def delete(self, request: HttpRequest, **kwargs):
        print(kwargs)
        # pk = kwargs.get("pk")
        # comment = ReComment.objects.get(pk=pk)
        #
        # if comment:
        #     comment.delete()
        #     return JsonResponse(True, status=200, safe=False)
        # return HttpResponseNotFound()
