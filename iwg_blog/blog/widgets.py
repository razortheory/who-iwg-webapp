from django.core.urlresolvers import reverse, reverse_lazy

from ..utils.forms.widgets import TabbedMarkdownWidget


class CustomMarkdownWidget(TabbedMarkdownWidget):
    preview_path = reverse_lazy('blog:article_preview_view')

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.update({
            'data-upload-image-url': reverse('upload_image_ajax'),
            'data-preview-parser-url': self.preview_path,
        })
        super(CustomMarkdownWidget, self).__init__(attrs)
