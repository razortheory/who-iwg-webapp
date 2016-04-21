"""
Urlize Extension for Python-Markdown
=============================================
Automatically text links parsing to html links
Examples:
    http://google.com
    www.google.co
    google.com (.com, .net, .org domains supported)
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import AtomicString, etree


class UrlizePattern(Pattern):
    RE = '(%s)' % '|'.join([
        r'<(?:f|ht)tps?://[^>]*>',
        r'\b(?:f|ht)tps?://[^)<>\s]+[^.,)<>\s]',
        r'\bwww\.[^)<>\s]+[^.,)<>\s]',
        r'[^(<\s]+\.(?:com|net|org)\b',
    ])

    def __init__(self, md):
        super(UrlizePattern, self).__init__(self.RE, md)

    def handleMatch(self, m):
        url = m.group(2)

        if url.startswith('<'):
            url = url[1:-1]

        text = url

        if not url.split('://')[0] in ('http', 'https', 'ftp'):
            if '@' in url and not '/' in url:
                url = 'mailto:' + url
            else:
                url = 'http://' + url

        el = etree.Element("a")
        el.set('href', url)
        el.set('target', '_blank')
        el.text = AtomicString(text)
        return el


class UrlizeExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['autolink'] = UrlizePattern(md)


def makeExtension(*args, **kwargs):
    return UrlizeExtension(*args, **kwargs)
