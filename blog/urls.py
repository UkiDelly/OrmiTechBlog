from django.urls import path

from blog.views import BlogListView, BlogCreateView, get_detail_view

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("<int:pk>/", get_detail_view, name="blog_detail"),
    path("create/", BlogCreateView.as_view(), name="blog_create"),
]
