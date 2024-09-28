from django.apps import AppConfig


# class BlogConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'blog'


   
class BlogConfig(AppConfig):
    name = 'apps.blog'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import apps.blog.signals

