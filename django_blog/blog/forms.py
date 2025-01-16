from django import forms
from .models import Post, Comment, Tag
from taggit.forms import TagField, TagWidget
from django.forms import widgets


class PostForm(forms.ModelForm):
    tags = TagField(widget=TagWidget())
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)


        
