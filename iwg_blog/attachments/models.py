from django.db import models

from ..blog.models import Article


class Document(models.Model):
    name = models.CharField(max_length=100)

    article = models.ForeignKey(Article, related_name='documents', blank=True, null=True)

    document_file = models.FileField(upload_to='documents')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class UploadedImage(models.Model):
    image_file = models.ImageField(upload_to='images')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'UploadedImage: %s' % self.image_file
