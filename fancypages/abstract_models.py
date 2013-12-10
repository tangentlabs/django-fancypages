from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from treebeard.mp_tree import MP_Node
from shortuuidfield import ShortUUIDField
from model_utils.managers import InheritanceManager

from .manager import PageManager
from .utils import get_container_names_from_template


class AbstractTreeNode(MP_Node):
    """
    Define the tree structure properties of the fancy page. This is a
    separate abstract class to make sure that it can be easily replaced
    by another tree handling library or none if needed.
    """
    name = models.CharField(_("Name"), max_length=255, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=255, db_index=True)
    image = models.ImageField(_('Image'), upload_to='fancypages/pages',
                              blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)

    _slug_separator = u'/'

    def save(self, update_slugs=True, *args, **kwargs):
        if update_slugs:
            parent = self.get_parent()
            slug = slugify(self.name)
            # If category has a parent, includes the parents slug in this one
            if parent:
                self.slug = '%s%s%s' % (
                    parent.slug, self._slug_separator, slug)
            else:
                self.slug = slug

        # Enforce slug uniqueness here as MySQL can't handle a unique index on
        # the slug field
        try:
            match = self.__class__.objects.get(slug=self.slug)
        except self.__class__.DoesNotExist:
            pass
        else:
            if match.id != self.id:
                raise ValidationError(
                    _("A page with slug '%(slug)s' already exists") % {
                        'slug': self.slug})
        super(AbstractTreeNode, self).save(*args, **kwargs)

    def move(self, target, pos=None):
        #:PEP8 -E501
        """
        Moves the current node and all its descendants to a new position
        relative to another node.

        See https://tabo.pe/projects/django-treebeard/docs/1.61/api.html
        """
        #:PEP8 +E501
        super(AbstractTreeNode, self).move(target, pos)
        # Update the slugs and full names of all nodes in the new subtree.
        # We need to reload self as 'move' doesn't update the current instance,
        # then we iterate over the subtree and call save which automatically
        # updates slugs.
        reloaded_self = self.__class__.objects.get(pk=self.pk)
        subtree = self.__class__.get_tree(parent=reloaded_self)
        for node in subtree:
            node.save()

    class Meta:
        abstract = True


class AbstractPageType(models.Model):
    uuid = ShortUUIDField(_("Unique ID"), db_index=True)
    name = models.CharField(_("Name"), max_length=128)
    slug = models.SlugField(_("Slug"), max_length=128)
    template_name = models.CharField(_("Template name"), max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(AbstractPageType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        app_label = 'fancypages'


class AbstractPageGroup(models.Model):
    """
    A page group provides a way to group fancy pages and retrieve only
    pages within a specific group.
    """
    uuid = ShortUUIDField(_("Unique ID"), db_index=True)
    name = models.CharField(_("Name"), max_length=128)
    slug = models.SlugField(_("Slug"), max_length=128, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(AbstractPageGroup, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        app_label = 'fancypages'


class AbstractFancyPage(models.Model):
    uuid = ShortUUIDField(_("Unique ID"), db_index=True)

    page_type = models.ForeignKey(
        'fancypages.PageType', verbose_name=_("Page type"),
        related_name="pages", null=True, blank=True)

    keywords = models.CharField(_("Keywords"), max_length=255, blank=True)

    containers = generic.GenericRelation('fancypages.Container')

    PUBLISHED, DRAFT, ARCHIVED = (u'published', u'draft', u'archived')
    STATUS_CHOICES = (
        (PUBLISHED, _("Published")),
        (DRAFT, _("Draft")),
        (ARCHIVED, _("Archived")),
    )
    status = models.CharField(
        _(u"Status"), max_length=15, choices=STATUS_CHOICES, blank=True)

    date_visible_start = models.DateTimeField(
        _("Visible from"), null=True, blank=True)
    date_visible_end = models.DateTimeField(
        _("Visible until"), null=True, blank=True)
    groups = models.ManyToManyField(
        'fancypages.PageGroup', verbose_name=_("Groups"), related_name="pages")

    # this is the default manager that should is
    # passed into subclasses when inheriting
    objects = PageManager()

    @property
    def is_visible(self):
        if self.status != AbstractFancyPage.PUBLISHED:
            return False

        now = timezone.now()
        if self.date_visible_start and self.date_visible_start > now:
            return False

        if self.date_visible_end and self.date_visible_end < now:
            return False

        return True

    def get_container_from_name(self, name):
        try:
            return self.containers.get(name=name)
        except models.get_model('fancypages', 'Container').DoesNotExist:
            return None

    def create_container(self, name):
        if self.containers.filter(name=name).count():
            return
        self.containers.create(name=name)

    @models.permalink
    def get_absolute_url(self):
        return ('fancypages:page-detail', (self.slug,), {})

    def __unicode__(self):
        return u"FancyPage '{0}'".format(self.name)

    def save(self, update_slugs=True, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.status:
            self.status = getattr(
                settings,
                'FP_DEFAULT_PAGE_STATUS',
                self.DRAFT
            )
        super(AbstractFancyPage, self).save(*args, **kwargs)

        try:
            template_name = self.page_type.template_name
        except AttributeError:
            template_name = settings.FANCYPAGES_DEFAULT_TEMPLATE

        existing_containers = [c.name for c in self.containers.all()]
        for cname in get_container_names_from_template(template_name):
            if cname not in existing_containers:
                self.containers.create(page_object=self, name=cname)

    class Meta:
        app_label = 'fancypages'
        abstract = True


class AbstractContainer(models.Model):
    template_name = 'fancypages/container.html'

    uuid = ShortUUIDField(_("Unique ID"), db_index=True)

    # this is the name of the variable used in the template tag
    # e.g. {% fancypages-container var-name %}
    name = models.SlugField(_("Variable name"), max_length=50, blank=True)
    title = models.CharField(_("Title"), max_length=100, blank=True)

    # this allows for assigning a container to any type of model. This
    # field is nullable as a container does not have to be assigned to a
    # model. In that case, it can be placed in any template by simply passing
    # the name into the template tag.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    page_object = generic.GenericForeignKey('content_type', 'object_id')

    @property
    def uid(self):
        #TODO: we should make this a proper UUID at some point
        return "{0}-{1}".format(self.name, self.id)

    def clean(self):
        if self.object_id and self.content_type:
            return

        # Don't allow draft entries to have a pub_date.
        container_exists = self.__class__.objects.filter(
            name=self.name,
            object_id=None,
            content_type=None,
        ).exists()
        if container_exists:
            raise ValidationError(
                "a container with name '{0}' already exists".format(self.name)
            )

    def get_template_names(self):
        return [self.template_name]

    @classmethod
    def get_container_by_name(cls, name, obj=None):
        """
        Get container of *obj* with the specified variable *name*. It
        assumes that *obj* has a ``containers`` attribute and returns
        the container with *name* or ``None`` if it cannot be found.
        """
        if not obj:
            container, __ = cls.objects.get_or_create(
                content_type=None,
                name=name,
                object_id=None,
            )
            return container

        object_type = ContentType.objects.get_for_model(obj)
        if object_type is None:
            return None

        ctn, __ = cls.objects.get_or_create(
            content_type=object_type,
            name=name,
            object_id=obj.id
        )
        return ctn

    @classmethod
    def get_containers(cls, obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return cls.objects.filter(
            content_type__id=obj_type.id,
            object_id=obj.id
        )

    def save(self, *args, **kwargs):
        self.clean()
        if not self.name:
            self.name = "%s-%s" % (
                self._meta.module_name,
                self.__class__.objects.count(),
            )
        return super(AbstractContainer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Container '%s' in '%s'" % (self.name, self.content_type)

    class Meta:
        abstract = True
        app_label = 'fancypages'


class AbstractContentBlock(models.Model):
    name = None
    code = None
    group = None
    template_name = None
    renderer_class = None
    form_class = None

    uuid = ShortUUIDField(_("Unique ID"), db_index=True)

    # we ignore the related names for each content block model
    # to prevent cluttering the container model. Also the look up has
    # to be done more efficient than through these attributes.
    container = models.ForeignKey(
        'fancypages.Container', verbose_name=_("Container"),
        related_name="blocks")

    display_order = models.PositiveIntegerField()

    objects = InheritanceManager()

    @classmethod
    def get_form_class(cls):
        return cls.form_class

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
        return [
            "fancypages/blocks/%s.html" % self._meta.module_name,
            "blocks/%s.html" % self._meta.module_name,
        ]

    def get_renderer_class(self):
        from fancypages.renderers import BlockRenderer
        return self.renderer_class or BlockRenderer

    def save(self, **kwargs):
        if self.display_order is None:
            self.display_order = self.container.blocks.count()

        try:
            db_block = self.__class__.objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            db_block = self

        db_container = db_block.container
        db_display_order = db_block.display_order

        super(AbstractContentBlock, self).save(**kwargs)

        if db_display_order != self.display_order \
           or self.container != db_container:
            self.fix_block_positions(db_display_order, db_container)

    def fix_block_positions(self, old_position, old_container):
        if self.container != old_container:
            for idx, block in enumerate(old_container.blocks.all()):
                block.display_order = idx
                block.save()

        if self.display_order > old_position:
            blocks = self.container.blocks.filter(
                ~models.Q(id=self.id) &
                models.Q(display_order__lte=self.display_order)
            )
            for idx, block in enumerate(blocks):
                block.display_order = idx
                block.save()

        else:
            blocks = self.container.blocks.filter(
                ~models.Q(id=self.id) &
                models.Q(display_order__gte=self.display_order)
            )
            for idx, block in enumerate(blocks):
                block.display_order = self.display_order + idx + 1
                block.save()

    def __unicode__(self):
        return "Block #%s" % self.id

    class Meta:
        abstract = True
