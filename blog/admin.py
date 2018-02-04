from django.contrib import admin
from .models import BlogPost, BlogPostComment
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(BlogPostComment)
