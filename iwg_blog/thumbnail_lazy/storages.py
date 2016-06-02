from __future__ import absolute_import

import base64

from storages.compat import Storage


class LazyStorage(Storage):
    """
    Base64 storage
    """
    def exists(self, name):
        return False

    def url(self, name):
        return 'data:image/jpeg;base64,%s' % name

    def save(self, name, content, max_length=None):
        return base64.b64encode(content.read())

lazy_storage = LazyStorage()
