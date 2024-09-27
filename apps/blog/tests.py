
from django.test import TestCase
from .models import Tag, Category, Author, Blog, Image

class TagModelTest(TestCase):
    def setUp(self):
        Tag.objects.create(name="Test Tag")

    def test_tag_creation(self):
        tag = Tag.objects.get(name="Test Tag")
        self.assertEqual(tag.name, "Test Tag")

