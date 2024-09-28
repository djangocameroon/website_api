from django.contrib import admin
from apps.blog.models.tag import Tag
from apps.blog.models.category import Category
from apps.blog.models.author import Author
from apps.blog.models.blog import Blog
from apps.blog.models.image import Image

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Image)
