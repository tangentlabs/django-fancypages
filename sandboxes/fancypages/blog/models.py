from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    """
    This is a simple blog post model that is used for example purposes only.
    """
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))

    author = models.ForeignKey('auth.User', verbose_name=_("Author"),
                               related_name="posts")

    date_created = models.DateTimeField(_("Date created"))

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
