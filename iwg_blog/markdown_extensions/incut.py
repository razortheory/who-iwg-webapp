"""
Python-Markdown extension designed specially for IWG article structure.
Wrap text blocks with `article__body-content` class and `article__body-incut` any other blocks.
=============================================
Input:
    <p>Hello world</p>
    <p>some other text</p>
    <img alt="alt_text" src="/media/images/andrew_galves_paORKUs.png" title="title">
Outputs:
    <div class="article__body-content">
        <p>Hello world</p>
        <p>some other text</p>
    </div>
    <div class="article__body-incut">
        <img alt="alt_text" src="/media/images/andrew_galves_paORKUs.png" title="title">
    </div>
"""

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from markdown import Extension
from markdown.postprocessors import Postprocessor


class IncutProcessor(Postprocessor):
    incut_tags = ['img', 'div', 'iframe', 'figure', 'table', 'pre', 'hr']
    incut_class = 'article__body-incut'
    incut_video_class = 'article__body-incut-video'
    content_class = 'article__body-content'

    def run(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        new_soup = BeautifulSoup()

        content = new_soup.new_tag('div', **{'class': self.content_class})

        for tag in soup.children:
            if isinstance(tag, NavigableString):
                continue

            if tag.name not in self.incut_tags and len(tag.contents) == 1 and tag.contents[0].name in self.incut_tags:
                tag = tag.contents[0]

            if tag.name in self.incut_tags:
                if len(content):
                    new_soup.append(content)
                    content = new_soup.new_tag('div', **{'class': self.content_class})

                klass = self.incut_class
                if tag.name == 'iframe':
                    klass += ' ' + self.incut_video_class

                incut = soup.new_tag('div', **{'class': klass})
                incut.append(tag)
                new_soup.append(incut)
            else:
                content.append(tag)

        if len(content):
            new_soup.append(content)

        return new_soup.decode()


class IncutExtenssion(Extension):
    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add(
            'incut', IncutProcessor(md), '_end',
        )


def makeExtension(*args, **kwargs):
    return IncutExtenssion(*args, **kwargs)
