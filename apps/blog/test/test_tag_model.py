
from django.test import TestCase
from apps.blog.models.tag import Tag
from apps.blog.models.category import Category
from apps.blog.models.author import Author
from apps.blog.models.blog import Blog
from apps.blog.models.image import Image

class TagModelTest(TestCase):
    def setUp(self):
        Tag.objects.create(name="Test Tag")

    def test_tag_creation(self):
        tag = Tag.objects.get(name="Test Tag")
        self.assertEqual(tag.name, "Test Tag")

