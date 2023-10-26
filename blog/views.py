from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from blog.forms import CommentForm, BlogForm, CategoryForm
from blog.models import Blog, Comment, Category


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
                | Q(tags__name__icontain=q)
            )
        return query_set


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm(
            initial={"author": self.request.user, "parent_comment": None, "blog": pk}
        )
        blog: Blog | None = get_object_or_404(Blog, pk=pk)
        comments = blog.comment_set.all()
        context["request"] = self.request
        context["blog"] = blog
        context["comments"] = comments
        context["comment_form"] = form
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_from"] = CategoryForm()
        return context

    # catch the form when press submit
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BlogForm
    model = Blog
    template_name = "blog/blog_form.html"

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("blog:blog_detail", kwargs=self.kwargs))
        return HttpResponseBadRequest


@login_required(login_url=reverse_lazy("accounts:login"))
def create_comment(request: HttpRequest, pk: int):
    comment_form = CommentForm(request.POST)
    parent_id = request.POST.get(key="parent_comment", default=None)
    parent_comment = None
    if parent_id is not None:
        parent_comment = Comment.objects.get(pk=parent_id)
    if comment_form.is_valid():
        print(comment_form.cleaned_data)

        Comment.objects.create(
            content=comment_form.cleaned_data["content"],
            author=request.user,
            blog=comment_form.cleaned_data["blog"],
            parent_comment=parent_comment,
        )
        return redirect("blog_detail", pk=pk)
    return JsonResponse({"result": comment_form.errors}, status=400)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    model = Comment

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            return super().post(request, *args, **kwargs)


def add_new_category(request: HttpRequest):
    category_form = CategoryForm(request.POST)
    if category_form.is_valid():
        category_form.save()

        category = Category.objects.all()
        return JsonResponse({"result": category}, status=200, safe=False)

    return JsonResponse({"result": category_form.errors}, status=400)


# TODO: JsonResponse를 사용해도 괜찮은지 물어보자

# class CommentView(View):
#
#     def get(self,request:HttpRequest, pk:int):
#         pass
#     ...
