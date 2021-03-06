import copy
import re

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from autoslug.utils import generate_unique_slug, slugify
from django_markdown.models import MarkdownField

from ..attachments.models import BaseDocument
from ..utils.base import markdown_to_text
from ..utils.models.fields import OrderedManyToManyField, AutoSlugField
from .helpers import ModelMeta
from .managers import ArticleManager, ArticleTagManager, PublishedArticleManager, SampleArticleManager


class Category(ModelMeta, models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    _metadata = {
        'title': 'name',
        'url': 'absolute_url',
    }

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail_view', args=(self.slug, ))

    @property
    def absolute_url(self):
        return self.get_absolute_url()


class Tag(ModelMeta, models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    objects = ArticleTagManager()

    _metadata = {
        'title': 'meta_name',
        'url': 'absolute_url',
    }

    @property
    def meta_name(self):
        return u"#%s" % self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail_view', args=(self.slug,))

    @property
    def absolute_url(self):
        return self.get_absolute_url()


class BaseArticle(ModelMeta, models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_READY_FOR_PUBLISH = 'for_pub'
    STATUS_PUBLISHED = 'published'

    CHOICES_STATUS = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_READY_FOR_PUBLISH, 'Ready for publishing'),
        (STATUS_PUBLISHED, 'Published')
    )

    title = models.CharField(max_length=130)

    cover_image = models.ImageField(upload_to='images')

    content = MarkdownField()
    words_count = models.IntegerField(default=0, editable=False)

    status = models.CharField(max_length=10, default=STATUS_DRAFT, choices=CHOICES_STATUS)

    hits = models.IntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    _metadata = {
        'title': 'title',
        'description': 'short_description_text',
        'image': 'cover_image_url',
        'image_width': 'cover_image_width',
        'image_height': 'cover_image_height',
        'url': 'absolute_url',
    }

    class Meta:
        abstract = True

        ordering = ['-published_at']

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        if self.status == self.STATUS_PUBLISHED:
            if not self.pk:
                self.published_at = timezone.now()
            else:
                self.published_at = models.Case(models.When(~models.Q(status=self.STATUS_PUBLISHED),
                                                            then=timezone.now()),
                                                default=self.published_at)

        self.words_count = len(re.findall(r"\S+", self.content_text))
        super(BaseArticle, self).save(**kwargs)

    @property
    def content_text(self):
        return markdown_to_text(self.content)

    @property
    def cover_image_url(self):
        return self.cover_image.url if self.cover_image else None

    @property
    def cover_image_width(self):
        return self.cover_image.width if self.cover_image else None

    @property
    def cover_image_height(self):
        return self.cover_image.height if self.cover_image else None

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        raise NotImplementedError()

    @classmethod
    def generate_slug(cls, title, instance_pk=None):
        original_slug = slugify(title)
        return generate_unique_slug(
            cls._meta.get_field_by_name('slug')[0],
            cls.all_objects.filter(pk=instance_pk).first() or cls(),
            original_slug,
            cls.all_objects
        )


class Article(BaseArticle):
    objects = ArticleManager()
    published = PublishedArticleManager()
    all_objects = models.Manager()

    categories = models.ManyToManyField(Category, related_name='articles')
    slug = AutoSlugField(
        populate_from='title',
        unique=True, db_index=True,
        editable=True, blank=True,
        help_text='optional; will be automatically populated from `title` field',
        manager=all_objects,
    )

    tags = OrderedManyToManyField(Tag, related_name='articles', blank=True)

    short_description = models.TextField(max_length=450)

    is_featured = models.BooleanField(default=False)
    is_sample = models.BooleanField(default=False, editable=False)

    _metadata = copy.copy(BaseArticle._metadata)
    _metadata['keywords'] = 'keywords'

    class Meta(BaseArticle.Meta):
        abstract = False

        permissions = (
            ('view_article_hits', 'Can view article hits'),
            ('change_article_slug', 'Can change article slug'),
        )

    def __init__(self, *args, **kwargs):
        """
        if `sample` provided, generate new Article from SampleArticle object
        """
        sample = kwargs.pop('sample', None)
        if sample:
            for field in ['title', 'category', 'cover_image', 'short_description', 'content']:
                kwargs[field] = getattr(sample, field)

        super(Article, self).__init__(*args, **kwargs)

    @property
    def keywords(self):
        return self.tags.values_list('slug', flat=True)

    def short_description_text(self):
        return self.short_description

    def get_absolute_url(self):
        return reverse('blog:article_detail_view', args=(self.slug,))


class SampleArticle(Article):
    objects = SampleArticleManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.is_sample = True
        super(SampleArticle, self).save(**kwargs)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    send_email = models.BooleanField(default=True)

    def __unicode__(self):
        return self.email


class ArticleDocument(BaseDocument):
    article = models.ForeignKey(Article, related_name='documents')
