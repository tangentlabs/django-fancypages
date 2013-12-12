from django.db import models
from django.utils.translation import ugettext_lazy as _

# To avoid that Twitter is required, we check for the library
# and if it isn't available, we don't register the TwitterBlock
# which means it can't be used.
try:
    import twitter_tag
except ImportError:
    TWITTER_AVAILABLE = False
else:
    TWITTER_AVAILABLE = False

from .content import ContentBlock
from ...library import register_content_block


@register_content_block
class VideoBlock(ContentBlock):
    name = _("Video")
    code = 'video'
    group = _("Media")
    template_name = "fancypages/blocks/video.html"

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


class TwitterBlock(ContentBlock):
    name = _("Twitter")
    code = 'twitter'
    group = _("Media")
    template_name = "fancypages/blocks/twitter.html"

    username = models.CharField(_('Twitter username'), max_length=50)
    max_tweets = models.PositiveIntegerField(_('Maximum tweets'), default=5)

    def __unicode__(self):
        if self.username:
            return u"Twitter user '@%s'" % self.username
        return u"Twitter: %s" % self.id

    class Meta:
        app_label = 'fancypages'


# If the twitter client is not installed, we are not registering the
# twitter block so that it can't be used.
if TWITTER_AVAILABLE:
    register_content_block(TwitterBlock)
