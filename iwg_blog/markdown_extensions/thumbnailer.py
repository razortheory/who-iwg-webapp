from bs4 import BeautifulSoup
from django.core.files.storage import default_storage
from markdown import Extension
from markdown.postprocessors import Postprocessor
from sorl.thumbnail import get_thumbnail

from iwg_blog.blog.watermarks_config import watermark_article
from ..attachments.models import UploadedImage


class ThumbnailerProcessor(Postprocessor):
    tags = {
        'img': 'src',
        'a': 'href'
    }

    def run(self, text):
        soup = BeautifulSoup(text, 'html.parser')

        matched_tags = {}
        for tag_obj in soup.findAll(self.tags.keys()):
            if self.tags[tag_obj.name] not in tag_obj.attrs:
                continue

            attr = tag_obj[self.tags[tag_obj.name]]
            if not attr.startswith(default_storage.base_url):
                continue

            key = attr[len(default_storage.base_url):]
            matched_tags[key] = matched_tags[key] if key in matched_tags else []
            matched_tags[key].append(tag_obj)

        for uploaded_image in UploadedImage.objects.filter(image_file__in=matched_tags.keys()):
            for tag_obj in matched_tags[uploaded_image.image_file]:
                tag_obj[self.tags[tag_obj.name]] = get_thumbnail(
                    uploaded_image.image_file, "1200", upscale=False, lazy=True, watermark=watermark_article
                ).url

        return soup.decode()


class ThumbnailerExtenssion(Extension):
    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add(
            'thumbnail', ThumbnailerProcessor(md), '_end',
        )


def makeExtension(*args, **kwargs):
    return ThumbnailerExtenssion(*args, **kwargs)
