from django import forms
from django.core.urlresolvers import reverse

import embedded_media

from .fields import MarkdownFormField, TagitField
from .models import Subscriber
from .widgets import AdminImageWidget, CustomMarkdownWidget


def set_attrs_for_field(field, attrs):
    field.widget.attrs = field.widget.attrs or {}
    field.widget.attrs.update(attrs)


class AutoSaveModelFormMixin(object):
    autosave_prefix = ''
    autosave_fields = []

    def __init__(self, *args, **kwargs):
        super(AutoSaveModelFormMixin, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            instance_identifier = instance.id
        else:
            instance_identifier = 'add'

        for field in self.autosave_fields:
            set_attrs_for_field(
                self.fields[field],
                {
                    'data-autosave': 'autosave_%s_%s:%s' % (self.autosave_prefix, instance_identifier, field),
                }
            )

    @property
    def media(self):
        media = super(AutoSaveModelFormMixin, self).media
        media.add_js(['admin/js/admin-models-autosave.js'])
        return media


class ArticleAdminForm(AutoSaveModelFormMixin, forms.ModelForm):
    autosave_prefix = 'blog_article'
    autosave_fields = ['content', 'short_description']

    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'content': CustomMarkdownWidget,
            'cover_image': AdminImageWidget,
        }
        field_classes = {
            'tags': TagitField,
            'content': MarkdownFormField,
        }
        help_texts = {
            'slug': ' '
        }

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

        self.fields['tags'].to_field_name = 'name'
        if self.instance.pk is not None:
            self.initial['tags'] = self.fields['tags'].prepare_value(self.instance.tags.all())

    @property
    def media(self):
        media = super(ArticleAdminForm, self).media
        media.add_js([
            embedded_media.JS('var populate_slug_opts={template_url: "%s", ajax_url: "%s", instance_pk: %s};' % (
                reverse('blog:article_detail_view', args=['dummy_slug']),
                reverse('blog:article_generate_slug_ajax'),
                self.instance.pk or 'undefined'
            )),
            'admin/js/admin-article-slug-control.js'
        ])
        return media


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
        error_messages = {
            'email': {
                'required': '',
            }
        }

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
    class Meta:
        model = Subscriber
        fields = ['email', ]

    def clean_email(self):
        email = self.cleaned_data['email']
        subscriber = Subscriber.objects.filter(email=email).first()
        if not subscriber:
            raise forms.ValidationError("Sorry, but we can't find this email address.")

        if not subscriber.send_email:
            raise forms.ValidationError("You have already unsubscribed from updates.")

        return email

    def save(self, commit=True):
        self.instance.send_email = False
        return super(UnsubscribeForm, self).save(commit)
