from django.urls import path

from comments.views import comment_list, AddComment

app_name = "comments"
urlpatterns = [
    path("", comment_list, name="comment_list"),
    path("add/", AddComment.as_view(), name="add_comment"),
]
