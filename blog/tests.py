from django.test import TestCase
from blog.models import BlogPost, BlogPostComment
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .forms import BlogPostCommentForm, BlogPostForm, UserForm
import sys
import captcha.conf.settings as captcha_settings

# Create your tests here.
class FormsTest(TestCase):
    """
    Testing forms
    """
    fixtures = ['fake_db.json']

    def test_UserForm(self):
        """
        Testing create new user's form
        """
        form = UserForm(data={'username':'Anton',
                              'email':'anton@anton.com',
                              'password':'anton12345'})
        self.assertTrue(form.is_valid())

    def test_addPostForm(self):
        """
        Testing add post's form
        """
        form = BlogPostForm(data={'title_text':'Title text',
                          'content_text':'Content text'})
        self.assertTrue(form.is_valid())

    def test_addPostCommentForm(self):
        """
        Testing add comment's form
        """
        form = BlogPostCommentForm(data={'content_text':'Content text'})


class BlogPostViewsTestCase(TestCase):
    fixtures = ['fake_db.json']

    def test_Index(self):
        """
        Testing the main page
        """
        my_response = self.client.get(reverse("blog:index"))
        self.assertEqual(my_response.status_code, 200)
        self.assertTrue('list' in my_response.context)
        self.assertTrue('num_pages' in my_response.context)

    def test_BlogPost(self):
        """
        Testing the detail page of some post
        """
        my_response = self.client.get(reverse("blog:post",
                                              kwargs={'blogpost_id': 1}))
        self.assertEqual(my_response.status_code, 200)
        self.assertTrue('blogpost' in my_response.context)
        self.assertTrue('comments' in my_response.context)
        blogpost = my_response.context['blogpost']
        self.assertEqual(blogpost.pk, 1)
        comments = my_response.context['comments']
        self.assertEqual(comments[0].pk, 1)

    def test_BlogPost404(self):
        """
        Testing that non-existent posts throw a 404
        """
        my_response = self.client.get(reverse("blog:post",
                                              kwargs={'blogpost_id': 999}))
        self.assertEqual(my_response.status_code, 404)

    # tests for RestAPI views
    def test_AllBlogPostAPI(self):
        my_response = self.client.get(reverse("allblogpostapi"))
        self.assertEqual(my_response.status_code, 200)

    def test_BlogPostAPI(self):
        my_response = self.client.get(reverse("blogpostapi",
                                              kwargs={'blogpost_id': 1}))
        self.assertEqual(my_response.status_code, 200)

    def test_BlogPostAPI404(self):
        my_response = self.client.get(reverse("blogpostapi",
                                              kwargs={'blogpost_id': 999}))
        self.assertEqual(my_response.status_code, 404)

    def test_UserBlogPostListAPI(self):
        my_response = self.client.get(reverse("userpostlist",
                                              kwargs={'user_id': 1}))
        self.assertEqual(my_response.status_code, 200)

    def test_UserBlogPostListAPI404(self):
        my_response = self.client.get(reverse("userpostlist",
                                              kwargs={'user_id': 999}))
        self.assertEqual(my_response.status_code, 404)
