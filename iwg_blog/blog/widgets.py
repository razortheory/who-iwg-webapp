from django.contrib.admin.widgets import AdminFileWidget
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import loader
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from django_markdown.utils import editor_js_initialization
from django_markdown.widgets import MarkdownWidget
from django_select2.forms import ModelSelect2TagWidget

from .models import Tag


class TabbedMarkdownWidget(MarkdownWidget):
    # Override to render content with some object context
    preview_path = None
    template_path = 'admin/tabbed_markitup.html'

    def render(self, name, value, attrs=None):
        editor_html = super(MarkdownWidget, self).render(name, value, attrs)
        attrs = self.build_attrs(attrs)
        preview_path = self.preview_path or reverse('django_markdown_preview')
        editor_initialization_html = editor_js_initialization(
            "#%s" % attrs['id'], previewParserPath=str(preview_path), previewInElement='#%s-preview iframe' % attrs['id']
        )

        return loader.get_template(self.template_path).render({
            'field_id': attrs['id'],
            'editor': editor_html,
            'editor_initialization': editor_initialization_html,
        })


class CustomMarkdownWidget(TabbedMarkdownWidget):
    preview_path = reverse_lazy('blog:article_preview_view')

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.update({
            'data-upload-image-url': reverse('upload_image_ajax'),
            'data-preview-parser-url': self.preview_path,
        })
        super(CustomMarkdownWidget, self).__init__(attrs)


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = u''
        if value and getattr(value, "url", None):
            output += u'<a href="%s" target="_blank"><img height="200" src="%s" alt="%s" /></a>' % (value.url, value.url, value)
        output += super(AdminFileWidget, self).render(name, value, attrs)
        return mark_safe(output)


class TagsSelect2AdminWidget(ModelSelect2TagWidget):
    search_fields = [
        'name__icontains',
    ]

    def get_queryset(self):
        return Tag.objects.all()

    def render_options(self, choices, selected_choices):
        output = ['<option></option>' if not self.is_required else '']

        queryset = self.get_queryset().filter(pk__in=selected_choices).order_by_array(selected_choices)
        choices = [(obj.pk, self.label_from_instance(obj))
                   for obj in queryset]

        for option_value, option_label in choices:
            output.append(self.render_option(map(force_text, selected_choices), option_value, option_label))
        return '\n'.join(output)

    def value_from_datadict(self, data, files, name):
        values = [value for value in data.getlist(name) if value]
        qs = self.get_queryset()
        int_values = []
        for val in values:
            try:
                int_values.append(int(val))
            except ValueError:
                pass

        existing_tags_pks = [str(pk) for pk in qs.filter(pk__in=int_values).values_list('pk', flat=True)]
        cleaned_pks = []
        for val in values:
            if val not in existing_tags_pks:
                val = qs.get_or_create(name=val)[0].pk
            cleaned_pks.append(val)
        return sorted(set(cleaned_pks), key=lambda x: cleaned_pks.index(x))
