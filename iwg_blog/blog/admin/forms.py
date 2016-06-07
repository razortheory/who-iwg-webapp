import copy

import embedded_media
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

from ...utils.forms.widgets import AdminImageWidget, LimitedTextarea
from ...utils.forms.fields import MarkdownFormField
from ...utils.forms.mixins import AutoSaveModelFormMixin
from ..fields import TagitField
from ..widgets import CustomMarkdownWidget


class BaseArticleAdminForm(AutoSaveModelFormMixin, forms.ModelForm):
    autosave_prefix = 'blog_article'
    autosave_fields = ['content', 'short_description']

    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'content': CustomMarkdownWidget,
            'cover_image': AdminImageWidget,
        }
        field_classes = {
            'content': MarkdownFormField,
        }
        help_texts = {
            'slug': ' ',
            'published_at': '%s Time' % settings.TIME_ZONE
        }

    @property
    def media(self):
        media = super(BaseArticleAdminForm, self).media
        media.add_js([
            embedded_media.JS('var populate_slug_opts={template_url: "%s", ajax_url: "%s", instance_pk: %s};' % (
                reverse('blog:article_detail_view', args=['dummy_slug']),
                reverse('blog:article_generate_slug_ajax'),
                self.instance.pk or 'undefined'
            )),
            'admin/js/admin-article-slug-control.js'
        ])
        return media


class ArticleAdminForm(BaseArticleAdminForm):
    class Meta(BaseArticleAdminForm.Meta):
        field_classes = copy.copy(BaseArticleAdminForm.Meta.field_classes)
        field_classes['tags'] = TagitField

        widgets = copy.copy(BaseArticleAdminForm.Meta.widgets)
        widgets['short_description'] = LimitedTextarea

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

        self.fields['tags'].to_field_name = 'name'
        # Work around https://code.djangoproject.com/ticket/17657
        if self.instance.pk is not None:
            self.initial['tags'] = self.fields['tags'].prepare_value(self.instance.tags.all())
