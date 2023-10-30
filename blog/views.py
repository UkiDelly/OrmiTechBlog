from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import (
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .forms import BlogForm
from .models import Blog, Category
from .comments.forms import CommentForm


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"
    ordering = "-created_at"

    def get_queryset(self):
        query_set = super().get_queryset()

        # reqeust의 GET 파라미터에서 'q'를 가져옵니다.
        q = self.request.GET.get("q")

        # 'q' 파라미터가 제공되었을 경우, 쿼리셋을 필터링한다.
        if q:
            query_set = query_set.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(categorys__name__icontains=q)
            )
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.all()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm(
            initial={"author": self.request.user,
                     "parent_comment": None, "blog": pk}
        )
        blog: Blog | None = get_object_or_404(Blog, pk=pk)
        comments = blog.comment_set.all().order_by("-created_at")
        context["request"] = self.request
        context["blog"] = blog
        context["comments"] = comments
        context["comment_form"] = form
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    model = Blog
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")

    # catch the form when press submit
    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
        return HttpResponseBadRequest(form.errors)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BlogForm
    model = Blog
    template_name = "blog/blog_form.html"

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("blog:blog_detail", kwargs=self.kwargs))
        return HttpResponseBadRequest


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "blog/blog_delete.html"
    success_url = reverse_lazy("blog:blog_list")


class MyBlogView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "blog/my_blog.html"
    context_object_name = "blogs"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = Blog.objects.filter(
            author=self.request.user).order_by("-created_at")
        return context
