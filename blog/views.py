from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm, BlogPostForm, BlogPostCommentForm
from .models import BlogPost, BlogPostComment
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import BlogPostSerializer, UserWithPostListSerializer

# Create your views here.


def get_paginator(request, list_of_items, count_per_page):
    """ Takes request, list of items and count of items per page.

    Returns correct list of items for current page, and
    a number of the page
    """
    paginator = Paginator(list_of_items, count_per_page)
    page = request.GET.get('page')
    try:
        current_post_list = paginator.page(page)
    except PageNotAnInteger:
        current_post_list = paginator.page(1)
    except EmptyPage:
        current_post_list = paginator.page(paginator.num_pages)
    num_pages = range(1, paginator.num_pages+1)
    return current_post_list, num_pages


def index(request):
    last_post_list = BlogPost.objects.order_by("-pub_date")[::-1]
    current_post_list, num_pages = get_paginator(request, last_post_list, 2)
    context = {
            'list': current_post_list,
            'num_pages': num_pages
    }
    return render(request, "blog/index.html", context)


def login_process(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('blog:index')

    return redirect('blog:index')


def logout_process(request):
    if request.user is not None:
        logout(request)
    return redirect('blog:index')


def search_process(request):
    search = request.GET['q']
    search_list = BlogPost.objects. \
        filter(Q(title_text__icontains=search)
        | Q(content_text__icontains=search)
        | Q(pub_date__contains=search))

    current_post_list, num_pages = get_paginator(request, search_list, 2)
    context = {
            'list': current_post_list,
            'num_pages': num_pages
    }
    return render(request, 'blog/search_results.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = "blog/registration_form.html"

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # don't add to db yet
            user = form.save(commit=False)
            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # return User object if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('blog:index')

        return render(request, self.template_name, {'form': form})


class BlogPostCreate(CreateView):
    """Creates new post """
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user_id = request.user.id
            new_post.save()
        return redirect('blog:post', blogpost_id=new_post.id)


def userPostList(request, user_name):
    """Returns render of all posts of a specific user"""
    if user_name == "my":
        user_id = request.user.id
    else:
        user_of_post = get_object_or_404(User, username=user_name)
        user_id = user_of_post.id

    post_list = BlogPost.objects.filter(user__id__exact=\
            user_id).order_by('-pub_date')[::-1]

    current_post_list, num_pages = get_paginator(request, post_list, 2)
    context = {
            'list': current_post_list,
            'num_pages': num_pages,
            'user_name': user_name
    }
    return render(request, "blog/user_post_list.html", context)


def blogPost(request, blogpost_id):
    form_class = BlogPostCommentForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user_id = request.user.id
            new_comment.blogpost_id = blogpost_id
            new_comment.save()
        return redirect('blog:post', blogpost_id=blogpost_id)
    form = form_class(None)
    template_name = "blog/BlogPost.html"
    blogpost_id = blogpost_id
    blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
    comments = BlogPostComment.objects.filter(blogpost__id__exact=\
            blogpost_id).order_by('-pub_date')
    context = {'blogpost': blogpost, 'comments': comments, 'form': form}
    return render(request, template_name, context)


class AllBlogPostAPI(APIView):
    """ Lists all objects of Blogpost class to api """

    def get(self, request):
        blogposts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogposts, many=True)
        return Response(serializer.data)

    def post(self):
        pass


@api_view(['GET'])
def blogPostAPI(request, blogpost_id):
    blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
    serializer = BlogPostSerializer(blogpost, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def userBlogPostListAPI(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = UserWithPostListSerializer(user)
    return Response(serializer.data)
