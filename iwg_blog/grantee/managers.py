from django.db import models


class PublishedGranteeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(PublishedGranteeManager, self).get_queryset(*args, **kwargs)\
            .filter(status=self.model.STATUS_PUBLISHED)
