from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.blog.models.tag import BlogTag
from apps.blog.models.blog import Blog


User = get_user_model()

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = BlogTag.objects.create(name="Test Tag")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Test Tag")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Test Tag")



class BlogModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="Jane", email="jane@example.com", password="password")
        self.blog = Blog.objects.create(
            title="Test Post",
            content="Some content here",
            author=self.author,
        )

    def test_blog_creation(self):
        self.assertEqual(self.blog.title, "Test Post")
        self.assertEqual(self.blog.author, self.author)

    def test_blog_str(self):
        self.assertEqual(str(self.blog), "Test Post")

    def test_blog_with_tags(self):
        tag = BlogTag.objects.create(name="Django")
        self.blog.tags.add(tag)
        self.assertTrue(self.blog.tags.filter(pk=tag.pk).exists())
