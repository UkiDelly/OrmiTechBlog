from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from blog.models import Blog, Category


class BlogForm(forms.ModelForm):
    thumbnail = forms.ImageField()
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = ["title", "thumbnail", "content", "categorys"]

    # add the current user to the model


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
