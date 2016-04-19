"""
Definition List Extension for Python-Markdown
=============================================
Added parsing of Figure captions to Python-Markdown.
A simple example:
    ![](http://placekitten.com/200/300)
    :   Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Praesent at consequat magna, faucibus ornare eros. sNam et
        mattis urna. Cras sodales, massa id gravida
Outputs:
    <figure>
        <img alt="" src="http://placekitten.com/200/300" />
        <figcaption>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Praesent at consequat magna, faucibus ornare eros. Nam et
            mattis urna. Cras sodales, massa id gravida</p>
        </figcaption>
    </figure>
"""

from markdown import Extension
from markdown.inlinepatterns import IMAGE_LINK_RE, IMAGE_REFERENCE_RE
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class FigcaptionProcessor(BlockProcessor):
    FIGURES = [IMAGE_LINK_RE, IMAGE_REFERENCE_RE]
    RE = re.compile(r'(^|\n)[ ]{0,3}:[ ]{1,3}(?P<caption>.*?)(\n|$)')
    FIGURES_RE = re.compile('|'.join(f for f in FIGURES))
    NO_INDENT_RE = re.compile(r'^[ ]{0,3}[^ :]')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        # pop the entire block as a single string
        raw_block = blocks.pop(0)

        # Get list of figure elements before the colon (:)
        m = self.RE.search(raw_block)

        # Get elements
        elements = raw_block[:m.start()]
        test_elements = self.FIGURES_RE.search(elements)

        if not test_elements:
            # This is not a figure item.
            blocks.insert(0, raw_block)
            return False

        # Get caption
        block = raw_block[m.end():]
        no_indent = self.NO_INDENT_RE.match(block)

        if no_indent:
            caption, theRest = (block, None)
        else:
            caption, theRest = self.detab(block)
        if caption:
            caption = '%s\n%s' % (m.group('caption'), caption)
        else:
            caption = m.group('caption')

        # Create figure
        figure = etree.SubElement(parent, 'figure')
        figure.text = elements

        # Add definition
        self.parser.state.set('fig')
        figcaption = etree.SubElement(figure, 'figcaption')
        self.parser.parseBlocks(figcaption, [caption])
        self.parser.state.reset()

        if theRest:
            blocks.insert(0, theRest)


class FigcaptionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('figcaption',
                                      FigcaptionProcessor(md.parser),
                                      '<ulist')


def makeExtension(*args, **kwargs):
    return FigcaptionExtension(*args, **kwargs)
