from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BlogPost(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    title_text = models.CharField(max_length=200)
    content_text = models.TextField()
    user = models.ForeignKey(User, related_name="blogposts",
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title_text


class BlogPostComment(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    content_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, related_name='comments',
                                 on_delete=models.CASCADE)
