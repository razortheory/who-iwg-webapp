"""
Embedding Extension for Python-Markdown
=============================================
Added youtube, vimeo, etc video embedding to Python-Markdown.
A simple example:
    ![embed?width=500&height=375](https://www.youtube.com/embed/02ZL5y2TY_o)
Outputs:
    <iframe allowfullscreen="" frameborder="0" height="375" mozallowfullscreen="" src="https://www.youtube.com/embed/02ZL5y2TY_o" webkitallowfullscreen="" width="500"></iframe>
"""
import re

from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension
from markdown.util import etree

from .utils import markdown_ordered_dict_prepend


class EmbeddingProcessor(ParagraphProcessor):
    RE = re.compile(r'!\[embed(\?(?P<params>.*))?\]\((?P<url>[^\)]+)\)')

    YOUTUBE_LINK_PATTERN = re.compile(r'youtu\.?be')
    VIMEO_LINK_PATTERN = re.compile(r'(https?://)?(www.)?(player.)?vimeo.com/([a-z]*/)*(?P<id>[0-9]{6,11})[?]?.*')

    YOUTUBE_PATTERNS = [
        re.compile(r'youtu\.be/(?P<id>\w+)'),  # youtu.be/<id>
        re.compile(r'(\?|&)v=(?P<id>\w+)'),  # ?v=<id> | &v=<id>
        re.compile(r'embed/(?P<id>\w+)'),  # embed/<id>
        re.compile(r'/v/(?P<id>\w+)'),  # /v/<id>
    ]

    YOUTUBE_EMBED_TEMPLATE = 'https://www.youtube.com/embed/%s'
    VIMEO_EMBED_TEMPLATE = 'https://player.vimeo.com/video/%s'

    def process_embed_url(self, url):
        youtube_match = self.YOUTUBE_LINK_PATTERN.search(url)
        if youtube_match:
            for pattern in self.YOUTUBE_PATTERNS:
                match = pattern.search(url)
                if not match:
                    continue

                return self.YOUTUBE_EMBED_TEMPLATE % match.group('id')

            return url

        vimeo_match = self.VIMEO_LINK_PATTERN.search(url)
        if vimeo_match:
            return self.VIMEO_EMBED_TEMPLATE % vimeo_match.group('id')

        return url

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        block_match = self.RE.match(block)

        el = etree.SubElement(parent, 'iframe')
        el.set('class', 'embed')
        el.set('webkitallowfullscreen', '')
        el.set('mozallowfullscreen', '')
        el.set('allowfullscreen', '')
        el.set('frameborder', '0')
        el.set('width', '100%')
        el.set('src', self.process_embed_url(block_match.groupdict()['url']))
        params = block_match.groupdict()['params'] or ''
        for param in params.split('&'):
            param = param.split('=')
            if len(param) == 2:
                el.set(*param)


class EmbeddingExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # Inserting to the top of inline patterns to avoid conflicts with images pattern
        markdown_ordered_dict_prepend(md.parser.blockprocessors, 'embed', EmbeddingProcessor(md.parser))


def makeExtension(*args, **kwargs):
    return EmbeddingExtension(*args, **kwargs)
