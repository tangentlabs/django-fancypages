from django.db import models
from django.utils.translation import ugettext_lazy as _

from .content import ContentBlock
from ...library import register_content_block


@register_content_block
class VideoBlock(ContentBlock):
    name = _("Video")
    code = 'video'
    group = _("Media")
    template_name = "fancypages/widgets/video.html"

    SOURCE_YOUTUBE = 'youtube'
    SOURCES = (
        (SOURCE_YOUTUBE, _('YouTube video')),
    )

    source = models.CharField(_('Video Type'), choices=SOURCES, max_length=50)
    video_code = models.CharField(_('Video Code'), max_length=50)

    def __unicode__(self):
        if self.source:
            return "Video '%s'" % self.video_code
        return "Video #%s" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class TwitterBlock(ContentBlock):
    name = _("Twitter")
    code = 'twitter'
    group = _("Media")
    template_name = "fancypages/widgets/twitter.html"

    username = models.CharField(_('Twitter username'), max_length=50)
    max_tweets = models.PositiveIntegerField(_('Maximum tweets'), default=5)

    def __unicode__(self):
        if self.username:
            return u"Twitter user '@%s'" % self.username
        return u"Twitter: %s" % self.id

    class Meta:
        app_label = 'fancypages'
