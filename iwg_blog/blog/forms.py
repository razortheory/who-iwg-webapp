from django import forms
from django.core.urlresolvers import reverse

from .fields import MarkdownFormField, OrderedModelMultipleChoiceField
from .models import Subscriber
from .widgets import ArticleContentMarkdownWidget, TagsSelect2AdminWidget


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

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

        preview_path = reverse('blog:article_preview_view')

        markdown_attrs = {
            'data-upload-image-url': reverse('upload_image_ajax'),
            'data-preview-parser-url': preview_path,
        }
        set_attrs_for_field(self.fields['content'], markdown_attrs)
        set_attrs_for_field(self.fields['short_description'], markdown_attrs)
        self.fields['content'].widget.preview_path = preview_path

    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'tags': TagsSelect2AdminWidget,
            'content': ArticleContentMarkdownWidget,
        }
        field_classes = {
            'tags': OrderedModelMultipleChoiceField,
            'content': MarkdownFormField,
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
