import copy

from django import forms
from django.core.urlresolvers import reverse

import embedded_media
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Layout, Field

from ..utils.forms import AutoSaveModelFormMixin
from .fields import MarkdownFormField, TagitField
from .models import Subscriber
from .widgets import AdminImageWidget, CustomMarkdownWidget, LimitedTextarea


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
            'published_at': 'UTC Time'
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
        if self.instance.pk is not None:
            self.initial['tags'] = self.fields['tags'].prepare_value(self.instance.tags.all())


class FlatPagesAdminForm(forms.ModelForm):
    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'content': CustomMarkdownWidget
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', ]

    def clean(self):
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']

        if Subscriber.objects.filter(email=email, send_email=True).exists():
            raise forms.ValidationError("You have already subscribed for updates.")

        return email

    def save(self, commit=True):
        try:
            self.instance = Subscriber.objects.get(email=self.instance.email)
            self.instance.send_email = True
        except Subscriber.DoesNotExist:
            pass
        return super(SubscribeForm, self).save(commit)


class UnsubscribeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'article__form'
        self.helper.layout = Layout(
            Field('send_email', type="hidden"),
            ButtonHolder(
                Submit('submit', 'Unsubscribe', css_class='article__form__button button')
            )
        )

    def clean_send_email(self):
        return False

    class Meta:
        model = Subscriber
        fields = ['send_email', ]
