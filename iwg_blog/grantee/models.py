from django.db import models

from django_markdown.models import MarkdownField


class Grantee(models.Model):
    name = models.CharField(max_length=255)

    content = MarkdownField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
