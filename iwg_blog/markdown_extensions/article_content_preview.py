"""
Article content preview Extension for Python-Markdown
=============================================
Input:
    ----article-content-preview----
    image: /media/images/tango_icon.png
    text: What are some of the myths - and facts - about vaccination?
    description: The diseases we can vaccinate against will return if we stop vaccination programmes.
    url: http://google.com
    -------------------------------
Outputs:
    <div class="article-content-preview">
        <div style="background-image:url(/media/images/tango_icon.png)"></div>
        <div class="article-content-preview__body">
            <h4 class="article-content-preview__title">What are some of the myths - and facts - about vaccination?</h4>
            <h4 class="article-content-preview__text">The diseases we can vaccinate against will return if we stop vaccination programmes.</h4>
            <h4 class="article-content-preview__link" href="http://google.com"><a href="http://google.com" target="_blank">google.com</a></h4>
        </div>
    </div>
"""

from urlparse import urlparse

import re

from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension
from markdown.util import etree, AtomicString


class ArticleContentPreviewGalleryProcessor(ParagraphProcessor):
    RE = re.compile(r'^[-]{3,}article-content-preview[-]{3,}\n(?P<data>(.*\n)+)[-]{10,}', re.MULTILINE)
    DATA_RE = re.compile(r'(?P<key>[^:]+):(?P<value>[^\n]+)')

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        for block in blocks:
            images_match = self.RE.match(block)
            if images_match:
                blocks.remove(block)
                article_content_preview = etree.SubElement(parent, 'div')
                article_content_preview.set('class', 'article-content-preview')

                data = {}
                for data_match in self.DATA_RE.finditer(images_match.group('data')):
                    data_dict = data_match.groupdict()
                    data[data_dict['key'].strip()] = data_dict['value'].strip()

                if 'image' in data:
                    image_item = etree.SubElement(article_content_preview, 'div')
                    image_item.set('style', 'background-image:url(%s)' % data['image'])

                body_item = etree.SubElement(article_content_preview, 'div')
                body_item.set('class', 'article-content-preview__body')
                body_title = etree.SubElement(body_item, 'h4')
                body_title.set('class', 'article-content-preview__title')
                body_title.text = data.get('text', '')

                if 'description' in data:
                    body_description = etree.SubElement(body_item, 'h4')
                    body_description.set('class', 'article-content-preview__text')
                    body_description.text = data.get('description', '')

                body_href = etree.SubElement(body_item, 'a')
                body_href.set('class', 'article-content-preview__link')
                body_href.set('target', '_blank')
                body_href.set('href', data['url'])
                body_href.text = AtomicString(urlparse(data['url']).netloc or data['url'])


class ArticleContentPreviewExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
            'article-content-preview', ArticleContentPreviewGalleryProcessor(md.parser), '<paragraph'
        )


def makeExtension(*args, **kwargs):
    return ArticleContentPreviewExtension(*args, **kwargs)

