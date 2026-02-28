from django.test import TestCase
from apps.blog.models.tag import Tag
from apps.blog.models.category import Category
from apps.blog.models.author import Author
from apps.blog.models.blog import Blog


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Test Tag")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Test Tag")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tech")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Tech")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Tech")


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe", bio="A writer")

    def test_author_creation(self):
        self.assertEqual(self.author.name, "John Doe")
        self.assertEqual(self.author.bio, "A writer")

    def test_author_str(self):
        self.assertEqual(str(self.author), "John Doe")


class BlogModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jane", bio="Author bio")
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

    def test_blog_with_tags_and_categories(self):
        tag = Tag.objects.create(name="Django")
        category = Category.objects.create(name="Web Dev")
        self.blog.tags.add(tag)
        self.blog.categories.add(category)
        self.assertTrue(self.blog.tags.filter(pk=tag.pk).exists())
        self.assertTrue(self.blog.categories.filter(pk=category.pk).exists())
