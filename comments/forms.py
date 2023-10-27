from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Comment
        fields = "__all__"
