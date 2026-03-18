from django.db.models import F

from apps.blog.models.blog import Blog, BlogLike

class BlogLikeService:

    @classmethod
    def toggle(cls, blog, user):
        try:
            like = BlogLike.objects.get(blog=blog, user=user)
            like.delete()
            Blog.objects.filter(pk=blog.pk).update(likes=F('likes') - 1)
            updated_blog = Blog.objects.get(pk=blog.pk)
            return {'liked': False, 'likes_count': updated_blog.likes}
        except BlogLike.DoesNotExist:
            BlogLike.objects.create(blog=blog, user=user)
            Blog.objects.filter(pk=blog.pk).update(likes=F('likes') + 1)
            updated_blog = Blog.objects.get(pk=blog.pk)
            return {'liked': True, 'likes_count': updated_blog.likes}

    @classmethod
    def has_liked(cls, blog, user):
        if not user or not user.is_authenticated:
            return False
        return BlogLike.objects.filter(blog=blog, user=user).exists()