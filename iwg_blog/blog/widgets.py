from django.contrib.admin.widgets import AdminFileWidget
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.utils import flatatt
from django.forms.widgets import CheckboxSelectMultiple
from django.template import loader
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django_markdown.utils import editor_js_initialization
from django_markdown.widgets import MarkdownWidget


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


class TagitWidget(CheckboxSelectMultiple):
    class Media:
        css = {
            'all': ['admin/css/jquery-ui.min.css', 'admin/css/jquery.tagit.css', 'admin/css/tag-it.custom.css']
        }
        js = ['admin/js/jquery-ui.min.js', 'admin/js/tag-it.min.js', 'admin/js/tag-it.setup.js']

    def __init__(self, attrs=None, autocomplete_url=None):
        final_attrs = {'class': 'tag-it'}

        if autocomplete_url:
            final_attrs['autocomplete-url'] = autocomplete_url

        if attrs is not None:
            final_attrs.update(attrs)

        super(TagitWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)

        output = [format_html('<ul{}>', flatatt(final_attrs))]
        output.extend([format_html('<li>{}</li>', label) for label in value])
        output.append('</ul>')

        return mark_safe('\n'.join(output))
