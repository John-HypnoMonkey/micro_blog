from rest_framework import serializers
from .models import BlogPost, BlogPostComment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'pk')


class BlogPostCommentSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = BlogPostComment
        fields = ('content_text', 'pub_date', 'user')


class BlogPostSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    comments = BlogPostCommentSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ('title_text', 'content_text', 'pub_date', 'user', 'comments')
        depth = 2


class UserWithPostListSerializer(serializers.ModelSerializer):

    blogposts = BlogPostSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'pk', 'blogposts')
        depth = 3
