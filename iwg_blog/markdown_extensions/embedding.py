"""
Embedding Extension for Python-Markdown
=============================================
Added youtube, vimeo, etc video embedding to Python-Markdown.
A simple example:
    ![embed?width=500&height=375](https://www.youtube.com/embed/02ZL5y2TY_o)
Outputs:
    <iframe allowfullscreen="" frameborder="0" height="375" mozallowfullscreen="" src="https://www.youtube.com/embed/02ZL5y2TY_o" webkitallowfullscreen="" width="500"></iframe>
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

from .utils import markdown_ordered_dict_prepend


class EmbeddingPattern(Pattern):
    RE = r'!\[embed(\?(?P<params>.*))?\]\((?P<url>[^\)]+)\)'

    def __init__(self, md):
        super(EmbeddingPattern, self).__init__(self.RE, md)

    def handleMatch(self, m):
        el = etree.Element('iframe')
        el.set('webkitallowfullscreen', '')
        el.set('mozallowfullscreen', '')
        el.set('allowfullscreen', '')
        el.set('frameborder', '0')
        el.set('src', m.groupdict()['url'])
        params = m.groupdict()['params'] or ''
        for param in params.split('&'):
            param = param.split('=')
            if len(param) == 2:
                el.set(*param)

        return el


class EmbeddingExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # Inserting to the top of inline patterns to avoid conflicts with images pattern
        markdown_ordered_dict_prepend(md.inlinePatterns, 'embed', EmbeddingPattern(md))


def makeExtension(*args, **kwargs):
    return EmbeddingExtension(*args, **kwargs)
