from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
        path("", views.index, name="index"),
        path("register/", views.UserFormView.as_view(), name='register'),
        path("login_process/", views.login_process, name='login_process'),
        path("logout/", views.logout_process, name="logout_process"),
        path("post/add", views.BlogPostCreate.as_view(), name='add-post'),
        path("posts/<user_name>", views.userPostList, name='userposts'),
        path("post/<int:blogpost_id>", views.blogPost, name="post"),
        path("search/", views.search_process, name="search_results"),
]
