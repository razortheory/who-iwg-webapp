"""
Images gallery Extension for Python-Markdown
=============================================
Input:
    ----images-gallery----
    ![alt_text](/media/images/andrew_galves_paORKUs.png "title")
    ![alt_text](/media/images/ellie_JrzWbFV.png "title")
    ![alt_text](/media/images/thomas_jbLH2AI.png)
Outputs:
    <div class="images-gallery">
        <div class="images-gallery-item"><img alt="alt_text" src="/media/images/andrew_galves_paORKUs.png" title="title"></div>
        <div class="images-gallery-item"><img alt="alt_text" src="/media/images/ellie_JrzWbFV.png" title="title"></div>
        <div class="images-gallery-item"><img alt="alt_text" src="/media/images/thomas_jbLH2AI.png"></div>
    </div>
"""

import re

from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension
from markdown.util import etree


class ImagesGalleryProcessor(ParagraphProcessor):
    RE = re.compile(r'^[-]{3,}images-gallery[-]{3,}\n(?P<data>(.*\n?)+)', re.MULTILINE)
    IMAGE_RE = re.compile(r'!\[(?P<alt_text>[^\]]+)\]\((?P<image_data>[^)]+)\)')
    COLUMNS_RE = re.compile(r'columns:[ ]?(?P<columns_num>\d+)\n')

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        images_match = self.RE.match(block)

        images_gallery_wrap = etree.SubElement(parent, 'div')
        images_gallery_wrap.set('class', 'images-gallery-wrapper')
        images_gallery = etree.SubElement(images_gallery_wrap, 'div')
        images_gallery.set('class', 'images-gallery')

        columns_match = self.COLUMNS_RE.match(images_match.group('data'))
        columns_num = int(columns_match.group('columns_num')) if columns_match else 2

        for image_match in self.IMAGE_RE.finditer(images_match.group('data')):
            image_dict = image_match.groupdict()
            image_data = image_dict['image_data']
            image_link = image_data.split()[0]

            gallery_item = etree.SubElement(images_gallery, 'div')
            gallery_item.set('class', 'images-gallery-item col-sm-%s' % (12/columns_num, ))

            gallery_item_link = etree.SubElement(gallery_item, 'a')
            gallery_item_link.set('href', image_link)
            gallery_item_link.set('target', '_blank')

            image = etree.SubElement(gallery_item_link, 'img')
            image.set('src', image_link)
            image.set('alt', image_dict['alt_text'])
            if len(image_data) > 1:
                image_title = ''.join(image_data.split()[1:]).strip(u' "')
                image.set('title', image_title)

        images_paginator = etree.SubElement(images_gallery_wrap, 'div')
        images_paginator.set('class', 'images-gallery-paginator')


class ImagesGalleryExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('images-gallery', ImagesGalleryProcessor(md.parser), '<paragraph')


def makeExtension(*args, **kwargs):
    return ImagesGalleryExtension(*args, **kwargs)
