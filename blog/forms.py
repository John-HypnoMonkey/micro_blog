from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField
from .models import BlogPost, BlogPostComment
import sys

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    if sys.argv[1] != 'test':
        captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title_text', 'content_text']


class BlogPostCommentForm(forms.ModelForm):

    class Meta:
        model = BlogPostComment
        fields = ['content_text']
