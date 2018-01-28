from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm, BlogPostForm
from .models import BlogPost
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.


def index(request):
    last_posts_list = BlogPost.objects.order_by("-pub_date")[::-1]
    paginator = Paginator(last_posts_list, 2)
    page = request.GET.get('page')
    try:
        current_post_list = paginator.page(page)
    except PageNotAnInteger:
        current_post_list = paginator.page(1)
    except EmptyPage:
        current_post_list = paginator.page(paginator.num_pages)
    num_pages = range(1, paginator.num_pages+1)

    context = {
            'list': current_post_list,
            'num_pages': num_pages
    }
    return render(request, "blog/index.html", context)


def login_process(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    # тут поставлю try except и возвращение ошибки если имя или пароль не те
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

    paginator = Paginator(search_list, 2)
    page = request.GET.get('page')
    try:
        current_post_list = paginator.page(page)
    except PageNotAnInteger:
        current_post_list = paginator.page(1)
    except EmptyPage:
        current_post_list = paginator.page(paginator.num_pages)
    num_pages = range(1, paginator.num_pages+1)

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
        return redirect('blog:index')


def userPostList(request, user_name):

    if user_name == "my":
        user_name = request.user.username

    post_list = BlogPost.objects.filter(user__username__contains=\
            user_name).order_by('-pub_date')[::-1]
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')
    try:
        current_post_list = paginator.page(page)
    except PageNotAnInteger:
        current_post_list = paginator.page(1)
    except EmptyPage:
        current_post_list = paginator.page(paginator.num_pages)
    num_pages = range(1, paginator.num_pages+1)

    context = {
            'list': current_post_list,
            'num_pages': num_pages,
            'user_name': user_name
    }
    return render(request, "blog/user_post_list.html", context)


def blogPost(request, blogpost_id):
    post = get_object_or_404(BlogPost, pk=blogpost_id)
    context = {'post': post}
    return render(request, "blog/BlogPost.html", context)
