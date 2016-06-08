from __future__ import unicode_literals

import logging

from sorl.thumbnail import default
from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail.compat import text_type
from sorl.thumbnail.conf import defaults as default_settings
from sorl.thumbnail.conf import settings
from sorl.thumbnail.images import DummyImageFile, ImageFile

from iwg_blog.thumbnail_lazy.storages import lazy_storage
from iwg_blog.thumbnail_lazy.tasks import generate_thumbnail_lazy

logger = logging.getLogger(__name__)


class LazyThumbnailBackend(ThumbnailBackend):
    """
    Backend for delaying convert process with celery.
    """
    def get_thumbnail(self, file_, geometry_string, **options):
        """
        Return thumbnails as base64 url if not exists in cache and delay convert process.
        Modified version of original get_thumbnail method.
        """
        if not options.pop('lazy', False):
            return super(LazyThumbnailBackend, self).get_thumbnail(file_, geometry_string, **options)

        logger.debug(text_type('Getting thumbnail for file [%s] at [%s]'), file_, geometry_string)

        if file_:
            source = ImageFile(file_)
        elif settings.THUMBNAIL_DUMMY:
            return DummyImageFile(geometry_string)
        else:
            return None

        # preserve image filetype
        if settings.THUMBNAIL_PRESERVE_FORMAT:
            options.setdefault('format', self._get_format(source))

        for key, value in self.default_options.items():
            options.setdefault(key, value)

        # For the future I think it is better to add options only if they
        # differ from the default settings as below. This will ensure the same
        # filenames being generated for new options at default.
        for key, attr in self.extra_options:
            value = getattr(settings, attr)
            if value != getattr(default_settings, attr):
                options.setdefault(key, value)

        name = self._get_thumbnail_filename(source, geometry_string, options)
        thumbnail = ImageFile(name, default.storage)
        cached = default.kvstore.get(thumbnail)

        if cached:
            return cached

        # MODIFIED CODE. Overwriting storage for lazy base64
        thumbnail = ImageFile(name, lazy_storage)
        generate_thumbnail_lazy.delay(file_, geometry_string, **options)
        # End of MODIFIED CODE

        try:
            source_image = default.engine.get_image(source)
        except IOError as e:
            logger.exception(e)
            if settings.THUMBNAIL_DUMMY:
                return DummyImageFile(geometry_string)
            else:
                # if S3Storage says file doesn't exist remotely, don't try to
                # create it and exit early.
                # Will return working empty image type; 404'd image
                logger.warn(text_type('Remote file [%s] at [%s] does not exist'),
                            file_, geometry_string)

                return thumbnail

        # We might as well set the size since we have the image in memory
        image_info = default.engine.get_image_info(source_image)
        options['image_info'] = image_info
        size = default.engine.get_image_size(source_image)
        source.set_size(size)

        try:
            self._create_thumbnail(source_image, geometry_string, options,
                                   thumbnail)
        finally:
            default.engine.cleanup(source_image)

        return thumbnail
