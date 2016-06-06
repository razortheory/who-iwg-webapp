import fcntl
import os

from django.core.files.base import ContentFile

from celery.task import task
from py_thumbnailer.exceptions import MimeTypeNotFoundException, ThumbnailerNotFoundException
from py_thumbnailer.thumbnail import create_thumbnail


@task
def generate_document_preview(document):
    path, filename = os.path.split(document.document_file.name)
    head, ext = os.path.splitext(filename)

    converter_lock = open('converter.lock', 'w+')

    try:
        fcntl.flock(converter_lock, fcntl.LOCK_EX)
        preview_buffer = create_thumbnail(document.document_file, resize_to=400)
    except (ThumbnailerNotFoundException, MimeTypeNotFoundException):
        return
    finally:
        fcntl.flock(converter_lock, fcntl.LOCK_UN)

    document.file_preview.save(u'%s.jpg' % head, ContentFile(preview_buffer.read()))


@task
def generate_document_previews(queryset):
    for document in queryset:
        generate_document_preview.delay(document)
