from django.utils import timezone
from django.db.models import F
from datetime import timedelta

from apps.blog.models.blog import Blog, BlogView

class BlogViewService:
    COOLDOWN_HOURS = 24  # same user/ip can only add a view once per 24h

    @classmethod
    def get_client_ip(cls, request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    @classmethod
    def should_track(cls, blog, ip_address, user=None):
        cooldown = timezone.now() - timedelta(hours=cls.COOLDOWN_HOURS)
        qs = BlogView.objects.filter(
            blog=blog,
            viewed_at__gte=cooldown
        )
        if user and user.is_authenticated:
            qs = qs.filter(user=user) | qs.filter(ip_address=ip_address)
        else:
            qs = qs.filter(ip_address=ip_address)
        return not qs.exists()

    @classmethod
    def track(cls, request, blog):
        ip = cls.get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        if not cls.should_track(blog, ip, user):
            return False

        BlogView.objects.create(
            blog=blog,
            ip_address=ip,
            user=user,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
        )

        # atomic increment to avoid race conditions
        Blog.objects.filter(pk=blog.pk).update(
            views=F('views') + 1
        )
        return True