from django.contrib import admin
from apps.blog.models.post import Category, Tag, Post

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)


