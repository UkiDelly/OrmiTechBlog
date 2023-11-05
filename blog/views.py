from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import (
    HttpResponseBadRequest, HttpRequest, HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    DeleteView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    TemplateView,
)

from blog.forms import BlogForm
from blog.models import Blog, Category
from comments.forms import CommentForm, ReCommentForm


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"
    ordering = "-created_at"

    def get_queryset(self):
        query_set = super().get_queryset()

        # reqeust의 GET 파라미터에서 'q'를 가져옵니다.
        q = self.request.GET.get("q")
        # 페이지 네이션
        page = self.request.GET.get("page")

        if q:
            query_set = Blog.objects.filter(Q(title__icontains=q))

        return query_set.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get("page")
        paginator = Paginator(context.get("blogs"), 6)
        context["blogs"] = paginator.get_page(page)
        context["most_like"] = Blog.objects.order_by('-likes').first()
        context["categorys"] = Category.objects.all()
        return context


class BlogSearchView(TemplateView):
    http_method_names = ["get"]
    template_name = "blog/search.html"

    def get(self, request: HttpRequest, **kwargs):
        query = self.request.GET.get("q")
        context = {'query': query}
        blog_list = Blog.objects.filter(
            Q(title__icontains=query) | Q(content__in=query))
        context["blogs"] = blog_list

        if not query:
            context["blogs"] = []
        return self.render_to_response(context)


def filter_category(request: HttpRequest, c_pk: int):
    category = get_object_or_404(Category, pk=c_pk)
    blog_list = Blog.objects.filter(
        categorys__name__icontains=category.name).order_by("-created_at")
    context = {"blogs": blog_list}
    context["category"] = category
    return render(request, "blog/category_search.html", context)


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm(initial={"author": self.request.user, "blog": pk})
        reply_form = ReCommentForm(initial={"author": self.request.user})
        blog: Blog | None = get_object_or_404(Blog, pk=pk)
        comments = blog.comment_set.all().order_by("-created_at")
        blog.view_count += 1
        blog.save()
        context["blog"] = blog
        context["comments"] = comments
        context["comment_form"] = form
        context["reply_form"] = reply_form
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    model = Blog
    template_name = "blog/blog_form.html"

    # catch the form when press submit
    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()

            new_blog_pk = form.instance.pk
            return redirect(reverse_lazy("blog:blog_detail", kwargs={"pk": new_blog_pk}))
        return HttpResponseBadRequest(form.errors)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BlogForm
    model = Blog
    template_name = "blog/blog_form.html"

    def get_context_data(self, **kwargs):
        blog = self.get_object()
        context = {"form": BlogForm(instance=blog)}
        return context

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
        user_blog = Blog.objects.filter(author=self.request.user).order_by(
            "-created_at"
        )

        context = {"blogs": user_blog}
        return context


class LikeUnlikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest, **kwargs):

        blog = Blog.objects.get(pk=kwargs["pk"])
        if blog is None:
            return HttpResponseNotFound()

        if blog.likes.contains(self.request.user):
            blog.likes.remove(self.request.user)
        else:
            blog.likes.add(self.request.user)
        return redirect(reverse_lazy("blog:blog_detail", kwargs={"pk": kwargs["pk"]}))
