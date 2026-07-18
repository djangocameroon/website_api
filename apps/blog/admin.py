from django.contrib import admin
from apps.blog.models.tag import BlogTag
from apps.blog.models.blog import Blog
from apps.blog.models.image import Image

admin.site.register(BlogTag)
admin.site.register(Blog)
admin.site.register(Image)
