from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BlogPost(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    title_text = models.CharField(max_length=200)
    content_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
