from __future__ import absolute_import, unicode_literals

import re

from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension
from markdown.util import etree


class EmbeddingProcessor(ParagraphProcessor):
    """ Process Media Embedding. """
    RE = re.compile(r'\[!embed(\?(?P<params>.*))?\]\((?P<url>[^\)]+)\)')

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        for block in blocks:
            match = self.RE.match(block)
            if match:
                blocks.remove(block)
                embedded = etree.SubElement(parent, 'iframe')
                embedded.set('webkitallowfullscreen', '')
                embedded.set('mozallowfullscreen', '')
                embedded.set('allowfullscreen', '')
                embedded.set('frameborder', '0')
                embedded.set('src', match.groupdict()['url'])
                params = match.groupdict()['params'] or ''
                for param in params.split('&'):
                    param = param.split('=')
                    if len(param) == 2:
                        embedded.set(*param)


class EmbeddingExtension(Extension):
    """ Add images gallery to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of ImagesGalleryExtension to BlockParser. """
        md.parser.blockprocessors.add('embed', EmbeddingProcessor(md.parser), '<paragraph')


def makeExtension(*args, **kwargs):
    return EmbeddingExtension(*args, **kwargs)
