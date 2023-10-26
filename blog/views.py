from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blog.models import Blog, Comment


# Create your views here.
# def blog_list(request: HttpRequest):
#     blogs = Blog.objects.order_by("-created_at").all()
#     blogs = [blog.toJson() for blog in blogs]
#
#     return JsonResponse({"result": blogs}, safe=False)


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"


# class BlogDetailView(DetailView):
#     model = Blog
#     template_name = "blog/blog_detail.html"
#     context_object_name = "blog"
#
#     def get_object(self, queryset=None):
#         blog = super().get_object(queryset)
#         return blog


def get_detail_view(reqeust: HttpRequest, pk: int):
    blog = Blog.objects.get(pk=pk)
    comment_query_set = Comment.objects.filter(blog_id__exact=pk).values()
    context = {"blog": blog, "comments": comment_query_set}
    return render(reqeust, "blog/blog_detail.html", context)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "tags"]
    success_url = reverse_lazy("blog_list")

    # catch the form when press submit
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
