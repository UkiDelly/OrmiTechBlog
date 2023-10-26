from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from blog.models import Blog


class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = ["title", "content", "tags"]

    # add the current user to the model
