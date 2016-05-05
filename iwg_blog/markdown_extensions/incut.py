from markdown import Extension
from markdown.postprocessors import Postprocessor
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString


class IncutProcessor(Postprocessor):
    incut_tags = ['div', 'iframe', 'figure', 'table', 'pre', 'hr']
    incut_class = 'article__body-incut'
    incut_video_class = 'article__body-incut-video'
    content_class = 'article__body-content'

    def run(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        new_soup = BeautifulSoup()

        content = new_soup.new_tag('div', **{'class': self.content_class})

        for tag in soup.children:
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
            elif isinstance(tag, NavigableString):
                tag.extract()
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
