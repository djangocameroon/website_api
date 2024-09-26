from django.contrib import admin
from .models.models import Tag, Category, Author, Blog, Image

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Image)
