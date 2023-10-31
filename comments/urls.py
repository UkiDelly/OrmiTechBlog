from django.urls import path

from comments.views import CommentListView, CommentView, ReplyCommentView

app_name = "comments"
urlpatterns = [
    path("", CommentListView.as_view(), name="comment_list"),
    path("add/", CommentView.as_view(), name="add_comment"),
    path("<int:comment_pk>/", CommentView.as_view(), name="edit_comment"),
    path("<int:comment_pk>/", CommentView.as_view(), name="delete_comment"),
    path(
        "<int:comment_pk>/reply/",
        ReplyCommentView.as_view(),
        name="add_reply_comment",
    ),
    path("reply/<int:reply_pk>/", ReplyCommentView.as_view(), name="reply_comment"),
]
