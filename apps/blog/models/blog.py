from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models.base_model import BaseModel
from apps.blog.models.tag import BlogTag

class Blog(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    cover_image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    read_time = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(
        BlogTag, related_name="blogs", default=None,
        verbose_name=_("Blog tags"), help_text=_("The tags for the blog"),)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "blogs"
        verbose_name = _("Blog")
        verbose_name_plural = _("Blog")

class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_views')
    user = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['blog', 'ip_address']),
            models.Index(fields=['blog', 'user']),
        ]

