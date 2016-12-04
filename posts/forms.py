from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    title = forms.CharField(label="제목")
    content = forms.CharField(widget=PagedownWidget(show_preview=False), label="내용")
    publish = forms.DateField(widget=DateInput(), label="게시일")

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]