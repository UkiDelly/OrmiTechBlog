from django import forms

from comments.models import Comment, ReComment


class CommentForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Comment
        fields = ["blog", "content", "author"]


class ReCommentForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = ReComment
        fields = "__all__"
