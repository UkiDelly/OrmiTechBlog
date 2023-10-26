from django.urls import path

from blog.views import (
    BlogCreateView,
    BlogListView,
    create_comment,
    BlogDetailView,
    BlogUpdateView,
    add_new_category,
)

app_name = "blog"
urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("create/", BlogCreateView.as_view(), name="blog_create"),
    path("<int:pk>/comment/new", create_comment, name="comment_new"),
    path("<int:pk>/update/", BlogUpdateView.as_view(), name="blog_update"),
    path("tag/new", add_new_category, name="tag_new"),
]
