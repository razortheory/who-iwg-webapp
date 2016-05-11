from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django_markdown.models import MarkdownField

from .managers import PublishedGranteeManager
from ..blog.utils import markdown_to_text
from ..blog.fields import AutoSlugField
from ..blog.models import BaseArticle


class Round(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(
        populate_from='name', editable=True, unique=True, blank=True,
        help_text='optional; will be automatically populated from `name` field'
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('grantee:round_view', args=(self.slug, ))


class Grantee(BaseArticle):
    objects = models.Manager()
    published = PublishedGranteeManager()

    round = models.ForeignKey(Round, related_name='articles')
    slug = AutoSlugField(
        populate_from='title',
        unique=True, db_index=True,
        editable=True, blank=True,
        help_text='optional; will be automatically populated from `title` field',
    )

    short_description = MarkdownField()

    category = {
        'name': 'Iwg Grantee',
        'get_absolute_url': reverse_lazy('grantee:grantee_list_view'),
    }

    class Meta(BaseArticle.Meta):
        abstract = False

        permissions = (
            ('view_grantee_hits', 'Can view grantee hits'),
            ('change_grantee_slug', 'Can change grantee slug'),
        )

    @property
    def short_description_text(self):
        return markdown_to_text(self.short_description)

    def get_absolute_url(self):
        return reverse('grantee:grantee_view', args=(self.slug, ))
