from django.urls import path, include

from blog.views import (
    BlogCreateView,
    BlogListView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
    MyBlogView, BlogSearchView, LikeUnlikeView, filter_category,
)

app_name = "blog"
urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("category/<int:c_pk>/", filter_category, name="category_search"),
    path("search/", BlogSearchView.as_view(), name="search"),
    path("myblog/", MyBlogView.as_view(), name="my_blog"),
    path("<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("create/", BlogCreateView.as_view(), name="blog_create"),
    path("<int:pk>/like/", LikeUnlikeView.as_view(), name="blog_like"),
    path("<int:pk>/update/", BlogUpdateView.as_view(), name="blog_update"),
    path("<int:pk>/delete/", BlogDeleteView.as_view(), name="blog_delete"),
    path("<int:pk>/comment/", include("comments.urls")),
]
