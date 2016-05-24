"""
Del/Ins Extension for Python-Markdown
=====================================
Wraps the inline content with ins/del tags.
-----
    This is ++added content++ and this is ~~deleted content~~

    <p>This is <ins>added content</ins> and this is <del>deleted content</del></p>
"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r"(\~\~)(.+?)(\~\~)"
INS_RE = r"(\+\+)(.+?)(\+\+)"


class DelInsExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('del', SimpleTagPattern(DEL_RE, 'del'), '<not_strong')
        md.inlinePatterns.add('ins', SimpleTagPattern(INS_RE, 'ins'), '<not_strong')


def makeExtension(configs=None):
    configs = configs or {}
    return DelInsExtension(configs=dict(configs))
