from django import forms
from django.core.urlresolvers import reverse

from django_markdown.widgets import MarkdownWidget
from django_select2.forms import Select2MultipleWidget

from .models import Subscriber
from .widgets import ArticleContentMarkdownWidget


def set_attrs_for_field(field, attrs):
    field.widget.attrs = field.widget.attrs or {}
    field.widget.attrs.update(attrs)


class MarkdownFormField(forms.CharField):
    widget = MarkdownWidget

    def __init__(self, *args, **kwargs):
        # Using default form initialization to prevent dirty widget overriding
        super(MarkdownFormField, self).__init__(*args, **kwargs)


class ArticleAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            preview_path = reverse('article_preview_view', args=[instance.id])
        else:
            preview_path = reverse('django_markdown_preview')

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
            'tags': Select2MultipleWidget,
            'content': ArticleContentMarkdownWidget,
        }
        field_classes = {
            'content': MarkdownFormField,
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

