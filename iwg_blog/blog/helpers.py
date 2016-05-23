from meta import settings
from meta.views import Meta as OldMeta


class Meta(OldMeta):
    image_width = None
    image_height = None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if not value:
            return
        if not hasattr(value, 'url'):
            if not value.startswith('http') and not value.startswith('/'):
                value = '%s%s' % (settings.IMAGE_URL, value)
            self._image = self.get_full_url(value)
            return

        self._image = value.url
        self.image_width = value.width
        self.image_height = value.height
