"""
Cite Extension for Python-Markdown
=============================================
Wraps the inline content surrounded by three double quotes into <cite> tags.
Usage
-----
    > Any long line that will still be quoted properly when it wraps.
    > \"""Quote author\"""

    <blockquote>
    <p>Any long line that will still be quoted properly when it wraps.<br>
    <cite>Quote author</cite></p>
    </blockquote>
"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern

CITE_RE = r'(\"{3})(.+?)\2'


class CiteExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('cite', SimpleTagPattern(CITE_RE, 'cite'), '<not_strong')


def makeExtension(configs=None):
    configs = configs or {}
    return CiteExtension(configs=dict(configs))
