"""
Article content preview Extension for Python-Markdown
=============================================
Input:
    ----big-link----
    image: /media/images/tango_icon.png or ![alt_text](/media/images/country-flags_abXgWVp.jpg "title")
    text: What are some of the myths - and facts - about vaccination?
    description: The diseases we can vaccinate against will return if we stop vaccination programmes.
    url: http://google.com
    -------------------------------
Outputs:
    <div class="article-content-preview">
        <div class="article-content-preview__thumbnail" style="background-image:url(/media/images/country-flags_abXgWVp.jpg)"></div>
        <div class="article-content-preview__body">
            <h4 class="article-content-preview__title">What are some of the myths - and facts - about vaccination?</h4>
            <h4 class="article-content-preview__text">The diseases we can vaccinate against will return if we stop vaccination programmes.</h4>
            <a class="article-content-preview__link" href="http://google.com" target="_blank">google.com</a>
        </div>
    </div>
"""

import re
from urlparse import urlparse

from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension
from markdown.inlinepatterns import IMAGE_LINK_RE
from markdown.util import AtomicString, etree


class BigLinkGalleryProcessor(ParagraphProcessor):
    RE = re.compile(r'^[-]{3,}big-link[-]{3,}\n(?P<data>(.*\n?)+)', re.MULTILINE)
    DATA_RE = re.compile(r'(?P<key>[^:]+):(?P<value>[^\n]+)')

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        block_match = self.RE.match(block)

        parent_div = etree.SubElement(parent, 'div')
        parent_div.set('class', 'article-content-preview_container')
        parent_link = etree.SubElement(parent_div, 'a')
        parent_link.set('class', 'article-content-preview_link')
        article_content_preview = etree.SubElement(parent_link, 'div')
        article_content_preview.set('class', 'article-content-preview')

        data = {}
        for data_match in self.DATA_RE.finditer(block_match.group('data')):
            data_dict = data_match.groupdict()
            data[data_dict['key'].strip()] = data_dict['value'].strip()

        if 'image' in data:
            image_tag_match = re.match(IMAGE_LINK_RE, data['image'])
            if image_tag_match:
                img_data = image_tag_match.group(9).split()
                data['image'] = img_data[0] if img_data else ''

            image_item = etree.SubElement(article_content_preview, 'div')
            image_item.set('style', 'background-image:url(%s)' % data['image'])
            image_item.set('class', 'article-content-preview__thumbnail')

        parent_link.set('href', data['url'])
        parent_link.set('target', '_blank')

        body_item = etree.SubElement(article_content_preview, 'div')
        body_item.set('class', 'article-content-preview__body')
        body_title = etree.SubElement(body_item, 'h4')
        body_title.set('class', 'article-content-preview__title')
        body_title.text = data.get('text', '')

        if 'description' in data:
            body_description = etree.SubElement(body_item, 'div')
            body_description.set('class', 'article-content-preview__text')
            body_description.text = data.get('description', '')

        body_href = etree.SubElement(body_item, 'span')
        body_href.set('class', 'article-content-preview__link')
        body_href.text = AtomicString(urlparse(data['url']).netloc or data['url'])


class BigLinkExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
            'big-link', BigLinkGalleryProcessor(md.parser), '<paragraph'
        )


def makeExtension(*args, **kwargs):
    return BigLinkExtension(*args, **kwargs)
