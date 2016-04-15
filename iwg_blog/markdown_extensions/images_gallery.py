"""
Images gallery Extension for Python-Markdown
=============================================
Input:
    ----images-gallery----
    ![alt_text](/media/images/andrew_galves_paORKUs.png "title")
    ![alt_text](/media/images/ellie_JrzWbFV.png "title")
    ![alt_text](/media/images/thomas_jbLH2AI.png "title")
    ----------------------
Outputs:
    <div class="images-gallery">
        <div class="images-gallery-item"><img alt="alt_text" src="/media/images/andrew_galves_paORKUs.png" title="title"></div>
        <div class="images-gallery-item"><img alt="alt_text" src="/media/images/ellie_JrzWbFV.png" title="title"></div>
        <div class="images-gallery-item"><img alt="alt_text" src="/media/images/thomas_jbLH2AI.png" title="title"></div>
    </div>
"""

import re

from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension
from markdown.util import etree


class ImagesGalleryProcessor(ParagraphProcessor):
    RE = re.compile(r'^[-]{3,}images-gallery[-]{3,}\n(?P<images>(.*\n)+)[-]{10,}', re.MULTILINE)
    IMAGE_RE = re.compile(r'!\[(?P<alt_text>[^\]]+)\]\((?P<image_url>[^ ]+) "(?P<title>[^"]+)"\)')

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        for block in blocks:
            images_match = self.RE.match(block)
            if images_match:
                blocks.remove(block)
                images_gallery = etree.SubElement(parent, 'div')
                images_gallery.set('class', 'images-gallery')

                for image_match in self.IMAGE_RE.finditer(images_match.group('images')):
                    image_dict = image_match.groupdict()

                    gallery_item = etree.SubElement(images_gallery, 'div')
                    gallery_item.set('class', 'images-gallery-item')

                    image = etree.SubElement(gallery_item, 'img')
                    image.set('src', image_dict['image_url'])
                    image.set('alt', image_dict['alt_text'])
                    image.set('title', image_dict['title'])


class ImagesGalleryExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('images-gallery', ImagesGalleryProcessor(md.parser), '<paragraph')


def makeExtension(*args, **kwargs):
    return ImagesGalleryExtension(*args, **kwargs)
