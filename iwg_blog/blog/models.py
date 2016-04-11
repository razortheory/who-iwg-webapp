from django.db import models

from autoslug import AutoSlugField
from django_markdown.models import MarkdownField

from .managers import CaseInsensitiveUniqueModelManager


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


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    objects = CaseInsensitiveUniqueModelManager(insensitive_unique_fields=['name', ])

    def __unicode__(self):
        return self.name


class Article(models.Model):
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

    class Meta:
        ordering = ['-created_at']
