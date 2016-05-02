from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

from .tasks import generate_document_preview
from ..blog.models import Article
from ..utils.file_types import get_file_type


class Document(models.Model):
    name = models.CharField(max_length=100)

    article = models.ForeignKey(Article, related_name='documents', blank=True, null=True)

    document_file = models.FileField(upload_to='documents')
    file_preview = models.ImageField(upload_to='documents/thumbnails', blank=True, null=True)

    is_featured = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        old_obj = None
        if self.pk:
            old_obj = Document.objects.get(pk=self.pk)

        super(Document, self).save(**kwargs)

        if not old_obj or old_obj.document_file != self.document_file:
            generate_document_preview.delay(self)

    def get_preview_url(self):
        if self.file_preview:
            return self.file_preview.url
        return static('attachments/images/other.png')

    def file_type_icon_url(self):
        file_type = get_file_type(self.document_file.name)
        return static('attachments/images/%s-icon.png' % file_type) if file_type else ''


class UploadedImage(models.Model):
    image_file = models.ImageField(upload_to='images')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'UploadedImage: %s' % self.image_file
