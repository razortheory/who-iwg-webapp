from django.contrib.admin.widgets import AdminFileWidget
from django.core.urlresolvers import reverse
from django.forms import CheckboxSelectMultiple, Textarea
from django.forms.utils import flatatt
from django.template import loader
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_markdown.utils import editor_js_initialization
from django_markdown.widgets import MarkdownWidget


class TabbedMarkdownWidget(MarkdownWidget):
    """
    Wrap markdown editor to bootstrap tabs.
    """
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


class AdminImageWidget(AdminFileWidget):
    """
    Admin image widget with preview.
    """
    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['class'] = attrs.get('class', '') + ' imagefile-input'

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id')

        url = value.url if value and getattr(value, "url", None) else ''
        output = u'<p><a href="%s" target="_blank">' \
                 u'<img style="max-height: 200px; margin-bottom: 5px;" id="%s_preview" src="%s"/></a></p>' \
                 % (url, self.id_for_label(id_), url)
        output += super(AdminFileWidget, self).render(name, value, attrs)
        return mark_safe(output)

    @property
    def media(self):
        media = super(AdminImageWidget, self).media
        media.add_js([
            'admin/js/adminImageWidget.js',
        ])
        return media


class TagitWidget(CheckboxSelectMultiple):
    """
    Tag input based on tag-it.js library.
    """
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

        output = [format_html(u'<ul{}>', flatatt(final_attrs))]
        output.extend([format_html(u'<li>{}</li>', label) for label in value])
        output.append(u'</ul>')

        return mark_safe('\n'.join(output))


class LimitedTextarea(Textarea):
    """
    Textarea with remained symbols indicator.
    """
    wrapper_template = u'<div class="limited-textarea">{} <div class="counter"></div></div>'

    class Media:
        css = {
            'all': ['admin/css/limited-textarea.css'],
        }
        js = ['admin/js/limited-textarea.js']

    def render(self, name, value, attrs=None):
        textarea = super(LimitedTextarea, self).render(name, value, attrs)
        return format_html(self.wrapper_template, textarea)
