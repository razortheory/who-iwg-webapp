from django.conf import settings as django_settings

from meta import settings
from meta.models import ModelMeta as OldModelMeta
from meta.views import Meta as OldMeta


class Meta(OldMeta):
    """
    Class to be used instead of Meta from `meta` module.
    Added default values support.
    Added image size attributes.
    """
    image_width = None
    image_height = None

    def __init__(self, **kwargs):
        for field_name, field_value in django_settings.META_DEFAULTS.items():
            kwargs[field_name] = kwargs.get(field_name) or field_value
        super(Meta, self).__init__(**kwargs)

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


class ModelMeta(OldModelMeta):
    meta_class = Meta

    def as_meta(self, request=None):
        """
        Method that generates the Meta object (from django-meta)
        """
        metadata = self.get_meta(request)
        meta = self.meta_class()
        for field, data in self._retrieve_data(request, metadata):
            setattr(meta, field, data)
        for field in ('og_description', 'twitter_description', 'gplus_description'):
            generaldesc = getattr(meta, 'description', False)
            if not getattr(meta, field, False) and generaldesc:
                setattr(meta, field, generaldesc)
        return meta
