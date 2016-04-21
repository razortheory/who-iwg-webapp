from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField
from django_markdown.models import MarkdownField
from markdown import markdown
from meta.models import ModelMeta

from .managers import ArticleManager, CaseInsensitiveUniqueModelManager, SampleArticleManager
from .utils import markdown_to_text


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
    STATUS_DRAFT = 'draft'
    STATUS_READY_FOR_PUBLISH = 'for_pub'
    STATUS_PUBLISHED = 'published'

    CHOICES_STATUS = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_READY_FOR_PUBLISH, 'Ready for publishing'),
        (STATUS_PUBLISHED, 'Published')
    )

    objects = ArticleManager()
    all_objects = models.Manager()

    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from='title',
        unique=True, db_index=True,
        editable=True, blank=True,
        help_text='optional; will be automatically populated from `title` field'
    )

    category = models.ForeignKey(Category, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)

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

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        if self.pk:
            old_obj = Article.all_objects.get(pk=self.pk)

            if old_obj.status != self.status and self.status == self.STATUS_PUBLISHED:
                self.published_at = timezone.now()

        self.words_count = len(self.content_text.split())
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
