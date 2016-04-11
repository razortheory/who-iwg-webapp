from django.db import models


class CaseInsensitiveUniqueModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.insensitive_unique_fields = kwargs.pop('insensitive_unique_fields', [])
        super(CaseInsensitiveUniqueModelManager, self).__init__(*args, **kwargs)

    def filter(self, **kwargs):
        for field_name in self.insensitive_unique_fields:
            if field_name in kwargs:
                kwargs['%s__iexact' % field_name] = kwargs[field_name]
                del kwargs[field_name]
        return super(CaseInsensitiveUniqueModelManager, self).filter(**kwargs)

    def get(self, **kwargs):
        for field_name in self.insensitive_unique_fields:
            if field_name in kwargs:
                kwargs['%s__iexact' % field_name] = kwargs[field_name]
                del kwargs[field_name]
        return super(CaseInsensitiveUniqueModelManager, self).get(**kwargs)