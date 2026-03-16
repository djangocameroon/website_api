from django.db import models
from django.utils.translation import gettext_lazy as _

class BlogTag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().lower()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = "blog_tags"
        verbose_name = _("Blog tag")
        verbose_name_plural = _("Blog tags")
  