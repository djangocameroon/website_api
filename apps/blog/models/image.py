from django.db import models
from apps.blog.models.blog import Blog

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    blog_post = models.ForeignKey(Blog, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.blog_post.title}"

