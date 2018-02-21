from django.test import TestCase
from blog.models import BlogPost, BlogPostComment
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your tests here.


class BlogPostViewsTestCase(TestCase):
    fixtures = ['fake_db.json']

    def test_Index(self):
        """
        Testing the main page
        """
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('list' in response.context)
        self.assertTrue('num_pages' in response.context)

    def test_BlogPost(self):
        """
        Testing the detail page of some post
        """
        response = self.client.get(reverse("blog:post",
                                           kwargs={'blogpost_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('blogpost' in response.context)
        self.assertTrue('comments' in response.context)
        blogpost = response.context['blogpost']
        self.assertEqual(blogpost.pk, 1)
        comments = response.context['comments']
        self.assertEqual(comments[0].pk, 1)

        # Ensure that non-existent posts throw a 404
        response = self.client.get(reverse("blog:post",
                                           kwargs={'blogpost_id': 999}))
        self.assertEqual(response.status_code, 404)
