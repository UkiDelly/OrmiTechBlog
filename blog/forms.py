from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from blog.models import Blog, Comment, Category


class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = ["title", "thumbnail", "content", "categorys"]

    # add the current user to the model


class CommentForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Comment
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
