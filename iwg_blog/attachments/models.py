from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

from ..utils.file_types import get_file_type
from .tasks import generate_document_preview


class BaseDocument(models.Model):
    name = models.CharField(max_length=100)

    document_file = models.FileField(upload_to='documents')
    file_preview = models.ImageField(upload_to='documents/thumbnails', blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        old_obj = None
        if self.pk:
            old_obj = self._default_manager.get(pk=self.pk)

        super(BaseDocument, self).save(**kwargs)

        if not old_obj or old_obj.document_file != self.document_file:
            generate_document_preview.delay(self)

    def get_preview_url(self):
        if self.file_preview:
            return self.file_preview.url
        return static('attachments/images/other.png')

    @property
    def file_type(self):
        return get_file_type(self.document_file.name)

    def file_type_icon_url(self):
        return static('attachments/images/%s-icon.png' % self.file_type) if self.file_type else ''


class Document(BaseDocument):
    is_featured = models.BooleanField('Visible', default=False)


class UploadedImage(models.Model):
    image_file = models.ImageField(upload_to='images')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'UploadedImage: %s' % self.image_file


class Link(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __unicode__(self):
        return self.title
