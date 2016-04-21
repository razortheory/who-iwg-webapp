from autoslug import AutoSlugField
from django_markdown.models import MarkdownField

from markdown import markdown

from meta.models import ModelMeta

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


from .managers import CaseInsensitiveUniqueModelManager


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    objects = CaseInsensitiveUniqueModelManager(insensitive_unique_fields=['name', ])

    def __unicode__(self):
        return self.name


class Article(ModelMeta, models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from='title',
        unique=True, db_index=True,
        editable=True, blank=True,
        help_text='optional; will be automatically populated from `title` field'
    )

    category = models.ForeignKey(Category, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)

    short_description = MarkdownField()
    content = MarkdownField()

    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    cover_image = models.ImageField(upload_to='images')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=None, null=True, blank=True)

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
        return reverse('article_detail_view', args=(self.id, ))

    def short_description_html(self):
        return markdown(self.short_description)

    _metadata = {
        'title': 'title',
        'description': 'short_description_html',
        'image': 'cover_image_url',
        'url': 'absolute_url',
        'keywords': 'keywords'
    }

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_published:
            already_exist_and_not_published = self.pk and not Article.objects.get(pk=self.pk).is_published
            if already_exist_and_not_published or not self.pk:
                self.published_at = timezone.now()

        super(Article, self).save(*args, **kwargs)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    send_email = models.BooleanField(default=True)

    def __unicode__(self):
        return self.email