import re
from autoslug.utils import slugify

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from django_markdown.models import MarkdownField
from markdown import markdown
from meta.models import ModelMeta

from .fields import AutoSlugField, OrderedManyToManyField
from .managers import ArticleManager, SampleArticleManager, ArticleTagManager, PublishedArticleManager
from .utils import markdown_to_text


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail_view', args=(self.slug, ))


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    objects = ArticleTagManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail_view', args=(self.slug,))


class Article(ModelMeta, models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_READY_FOR_PUBLISH = 'for_pub'
    STATUS_PUBLISHED = 'published'

    CHOICES_STATUS = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_READY_FOR_PUBLISH, 'Ready for publishing'),
        (STATUS_PUBLISHED, 'Published')
    )

    objects = ArticleManager()
    published = PublishedArticleManager()
    all_objects = models.Manager()

    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from='title',
        unique=True, db_index=True,
        editable=True, blank=True,
        help_text='optional; will be automatically populated from `title` field',
        manager=all_objects,
    )

    category = models.ForeignKey(Category, related_name='articles')
    tags = OrderedManyToManyField(Tag, related_name='articles', blank=True)

    cover_image = models.ImageField(upload_to='images')

    short_description = MarkdownField()
    content = MarkdownField()
    words_count = models.IntegerField(default=0, editable=False)

    status = models.CharField(max_length=10, default=STATUS_DRAFT, choices=CHOICES_STATUS)
    is_featured = models.BooleanField(default=False)
    is_sample = models.BooleanField(default=False, editable=False)

    hits = models.IntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, editable=False)

    def __init__(self, *args, **kwargs):
        sample = kwargs.pop('sample', None)
        if sample:
            for field in ['title', 'category', 'cover_image', 'short_description', 'content']:
                kwargs[field] = getattr(sample, field)

        super(Article, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        if self.pk:
            old_obj = Article.all_objects.get(pk=self.pk)

            if old_obj.status != self.status and self.status == self.STATUS_PUBLISHED:
                self.published_at = timezone.now()

        self.words_count = len(re.findall(r"\S+", self.content_text))
        super(Article, self).save(**kwargs)

    @property
    def short_description_text(self):
        return markdown_to_text(self.short_description)

    @property
    def content_text(self):
        return markdown_to_text(self.content)

    @property
    def cover_image_url(self):
        return self.cover_image.url

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    @property
    def keywords(self):
        return self.tags.values_list('slug', flat=True)

    def get_absolute_url(self):
        return reverse('blog:article_detail_view', args=(self.slug, ))

    def short_description_html(self):
        return markdown(self.short_description)

    @classmethod
    def generate_slug(cls, title, instance_pk=None):
        original_slug = slugify(title)
        field = cls._meta.get_field_by_name('slug')[0]
        if field.max_length < len(original_slug):
            original_slug = original_slug[:field.max_length]

        slug = original_slug
        index = 0
        # keep changing the slug until it is unique
        while True:
            # find instances with same slug
            rivals = cls.all_objects.filter(slug=slug)
            if instance_pk:
                rivals = rivals.exclude(pk=instance_pk)

            if not rivals:
                # the slug is unique, no model uses it
                return slug

            # the slug is not unique; change once more
            index += 1

            # ensure the resulting string is not too long
            tail_length = len(field.index_sep) + len(str(index))
            combined_length = len(original_slug) + tail_length
            if field.max_length < combined_length:
                original_slug = original_slug[:field.max_length - tail_length]

            # re-generate the slug
            data = dict(slug=original_slug, sep=field.index_sep, index=index)
            slug = '%(slug)s%(sep)s%(index)d' % data

            # ...next iteration...

    _metadata = {
        'title': 'title',
        'description': 'short_description_html',
        'image': 'cover_image_url',
        'url': 'absolute_url',
        'keywords': 'keywords'
    }

    class Meta:
        ordering = ['-published_at']
        permissions = (
            ('view_article_hits', 'Can view article hits'),
            ('change_article_slug', 'Can change article slug'),
        )


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
