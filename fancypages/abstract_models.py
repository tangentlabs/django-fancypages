# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language, ugettext_lazy as _

from shortuuid import uuid
from treebeard.mp_tree import MP_Node
from shortuuidfield import ShortUUIDField
from model_utils.managers import InheritanceManager

from . import mixins
from .utils import unicode_slugify as slugify
from .managers import PageManager, ContainerManager
from .utils import get_container_names_from_template


class AbstractPageNode(MP_Node):
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

    @models.permalink
    def get_absolute_url(self):
        return ('fancypages:page-detail', (), {'slug': self.slug})

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
        super(AbstractPageNode, self).save(*args, **kwargs)

    def move(self, target, pos=None):
        """
        Moves the current node and all its descendants to a new position
        relative to another node.

        See https://tabo.pe/projects/django-treebeard/docs/1.61/api.html
        """
        super(AbstractPageNode, self).move(target, pos)
        # Update the slugs and full names of all nodes in the new subtree.
        # We need to reload self as 'move' doesn't update the current instance,
        # then we iterate over the subtree and call save which automatically
        # updates slugs.
        reloaded_self = self.__class__.objects.get(pk=self.pk)
        subtree = self.__class__.get_tree(parent=reloaded_self)
        for node in subtree:
            node.save()
    move.alters_data = True

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.slug)

    class Meta:
        app_label = 'fancypages'
        abstract = True


class AbstractPageType(models.Model):
    uuid = ShortUUIDField(verbose_name=_("Unique ID"), db_index=True)
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
    uuid = ShortUUIDField(verbose_name=_("Unique ID"), db_index=True)
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
    uuid = ShortUUIDField(verbose_name=_("Unique ID"), db_index=True)
    # this field has to be NULLABLE for backwards compatibility but should
    # never be left blank (hence, blank=False). We might be able to remove this
    # at some point but migrations make it impossible to change without a
    # default value. There's no sensible default, so we leave it nuu
    node = models.OneToOneField(
        settings.FP_NODE_MODEL, verbose_name=_("Tree node"),
        related_name='page', null=True)

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

    @models.permalink
    def get_edit_page_url(self):
        """ Get the dashboard URL for updating the page. """
        return ("fp-dashboard:page-update", (), {'pk': self.pk})

    @models.permalink
    def get_add_child_url(self):
        """ Get the dashboard URL for adding a child page. """
        return ("fp-dashboard:child-page-create", (), {'parent_pk': self.pk})

    @models.permalink
    def get_delete_page_url(self):
        """ Get the dashboard URL fo deleting this page. """
        return ("fp-dashboard:page-delete", (), {'pk': self.pk})

    @classmethod
    def _split_kwargs(cls, dct, prefix="node__"):
        prefixed = {}
        cleaned = {}
        for key, value in dct.iteritems():
            if key.startswith(prefix):
                prefixed[key.replace(prefix, '')] = value
            else:
                cleaned[key] = value
        return prefixed, cleaned

    def add_child(self, **kwargs):
        node_kwargs, page_kwargs = self._split_kwargs(kwargs)
        page_kwargs['node'] = self.node.add_child(**node_kwargs)
        return self.__class__.objects.create(**page_kwargs)
    add_child.alters_data = True

    @classmethod
    def add_root(cls, **kwargs):
        from .utils import get_node_model
        node_kwargs, page_kwargs = cls._split_kwargs(kwargs)
        page_kwargs['node'] = get_node_model().add_root(**node_kwargs)
        return cls.objects.create(**page_kwargs)

    def get_children(self):
        """
        Get all child pages as a queryset. It uses the related node's
        ``get_children`` method from ``treebeard`` but returning a queryset of
        <FancyPage fancypages.models.FancyPage> objects instead of their nodes.

        :return: Queryset of <FancyPage fancypages.models.FancyPage> objects.
        """
        nodes = self.node.get_children()
        return self.__class__.objects.filter(node__in=nodes)

    def delete(self, using=None):
        """
        Deletes the instance of ``FancyPage`` and makes sure that the related
        ``PageNode`` is deleted as well. This should usually be handled by the
        ``on_delete`` argument on the ``ForeignKey`` field but in this instance
        it doesn't take effect. For the time being, the node object is delete
        after the page has been removed.
        """
        node = self.node
        super(AbstractFancyPage, self).delete(using)
        node.delete()
    delete.alters_data = True

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError
        try:
            return getattr(self.node, name)
        except AttributeError:
            pass
        raise AttributeError(
            "neither '{}' nor '{}' have an attribute '{}".format(
                self.__class__, self.node.__class__, name))

    def get_container_from_name(self, name):
        try:
            return self.containers.get(name=name)
        except models.get_model('fancypages', 'Container').DoesNotExist:
            return None

    def create_container(self, name):
        if self.containers.filter(name=name).count():
            return
        self.containers.create(name=name)
    create_container.alters_data = True

    def __unicode__(self):
        return u"FancyPage '{0}'".format(self.name)

    def save(self, update_slugs=True, *args, **kwargs):
        """
        Saving this page has several additional responsibilities to ensure
        the consistency of the data. Before actually saving the model to the
        database, it is ensured that *slug* and *status* are set on the page
        if either of them is not defined. If not set, the slug is generated
        from the page name. If the status is not set, the default status
        defined in ``FP_DEFAULT_PAGE_STATUS`` is used.
        After saving, all containers specified in the template for this page
        that don't exist are created. Using the current language code used in
        the overall context of this model.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.status:
            self.status = getattr(
                settings, 'FP_DEFAULT_PAGE_STATUS', self.DRAFT)

        super(AbstractFancyPage, self).save(*args, **kwargs)

        language_code = get_language()
        for cname in self._get_missing_containers(language_code=language_code):
            self.containers.create(
                page_object=self, name=cname, language_code=language_code)

    def _get_missing_containers(self, language_code=None):
        language_code = language_code or get_language()

        try:
            template_name = self.page_type.template_name
        except AttributeError:
            template_name = settings.FANCYPAGES_DEFAULT_TEMPLATE

        cnames = self.containers.filter(
            language_code=language_code).values_list('name')
        existing_containers = [i[0] for i in cnames]

        for cname in get_container_names_from_template(template_name):
            if cname not in existing_containers:
                yield cname

    class Meta:
        app_label = 'fancypages'
        abstract = True


class AbstractContainer(mixins.TemplateNamesModelMixin, models.Model):
    template_name = 'fancypages/container.html'

    uuid = ShortUUIDField(verbose_name=_("Unique ID"), db_index=True)

    # this is the name of the variable used in the template tag
    # e.g. {% fancypages-container var-name %}
    name = models.SlugField(_("Variable name"), max_length=50, blank=True)
    title = models.CharField(_("Title"), max_length=100, blank=True)
    language_code = models.CharField(
        _("Language"), max_length=7, default=get_language())

    # this allows for assigning a container to any type of model. This
    # field is nullable as a container does not have to be assigned to a
    # model. In that case, it can be placed in any template by simply passing
    # the name into the template tag.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    page_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = ContainerManager()

    def clean(self):
        if self.object_id and self.content_type:
            return
        # Don't allow draft entries to have a pub_date.
        container_exists = self.__class__.objects.filter(
            name=self.name, object_id=None, content_type=None).exists()
        if container_exists:
            raise ValidationError(
                "a container with name '{0}' already exists".format(self.name))

    @classmethod
    def get_container_by_name(cls, name, obj=None, language_code=u''):
        """
        Get container of *obj* with the specified variable *name*. It
        assumes that *obj* has a ``containers`` attribute and returns
        the container with *name* or ``None`` if it cannot be found.
        """
        filters = {
            'name': name, 'language_code': language_code or get_language()}
        if not obj:
            container, __ = cls.objects.get_or_create(**filters)
            return container

        object_type = ContentType.objects.get_for_model(obj)
        if object_type is None:
            return None

        filters['content_type'] = object_type
        filters['object_id'] = obj.id
        ctn, __ = cls.objects.get_or_create(**filters)
        return ctn

    def save(self, *args, **kwargs):
        self.clean()
        # make sure that we have a UUID set, we might need it before it will
        # be automatically generated by the ShortUUIDField
        if not self.uuid:
            self.uuid = unicode(uuid())
        # Check if we have a name, if not we generate a name from the model
        # name and the UUID of this block. This avoids collision when
        # auto-generating new models without explicit name
        if not self.name:
            self.name = "{}-{}".format(self._meta.module_name, self.uuid)
        return super(AbstractContainer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Container '{}' in '{}' [{}]".format(
            self.name, self.content_type, self.language_code)

    class Meta:
        abstract = True
        app_label = 'fancypages'


class AbstractContentBlock(mixins.TemplateNamesModelMixin, models.Model):
    name = None
    code = None
    group = None
    template_name = None
    renderer_class = None
    form_class = None

    default_template_names = [
        "fancypages/blocks/{module_name}.html", "blocks/{module_name}.html"]

    uuid = ShortUUIDField(verbose_name=_("Unique ID"), db_index=True)

    # we ignore the related names for each content block model
    # to prevent cluttering the container model. Also the look up has
    # to be done more efficient than through these attributes.
    container = models.ForeignKey(
        'fancypages.Container', verbose_name=_("Container"),
        related_name="blocks")

    display_order = models.PositiveIntegerField()

    objects = InheritanceManager()

    @property
    def language_code(self):
        try:
            return self.container.language_code
        except AbstractContainer.DoesNotExist:
            pass
        return u''

    @classmethod
    def get_form_class(cls):
        return cls.form_class

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
    fix_block_positions.alters_data = True

    def __unicode__(self):
        return "Block #%s" % self.id

    class Meta:
        abstract = True
