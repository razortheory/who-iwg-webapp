from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from django_markdown.utils import editor_js_initialization
from django_markdown.widgets import MarkdownWidget


class ArticleContentMarkdownWidget(MarkdownWidget):
    # Override to render content with some object context
    preview_path = None

    def render(self, name, value, attrs=None):
        html = super(MarkdownWidget, self).render(name, value, attrs)
        attrs = self.build_attrs(attrs)
        if self.preview_path:
            preview_path = self.preview_path
        else:
            preview_path = reverse('django_markdown_preview')

        html += editor_js_initialization(
            "#%s" % attrs['id'], previewParserPath=preview_path
        )
        return mark_safe(html)
