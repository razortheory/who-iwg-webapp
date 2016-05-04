from markdown import Extension
from markdown.postprocessors import Postprocessor
from bs4 import BeautifulSoup
from bs4.element import Tag


class IncutProcessor(Postprocessor):
    incut_tags = ['div', 'iframe', 'figure', 'table', 'pre', 'hr']
    incut_class = 'article__body-incut'
    content_class = 'article__body-content'

    def run(self, text):
        soup = BeautifulSoup(text, 'html.parser')

        content = soup.new_tag('div', **{'class': self.content_class})

        try:
            tag = soup.children.next()

            while tag:
                if tag.name in self.incut_tags:
                    if len(content):
                        soup.append(content)
                        content = soup.new_tag('div', **{'class': self.content_class})

                    incut = soup.new_tag('div', **{'class': self.incut_class})
                    incut.append(tag)
                    soup.append(incut)
                else:
                    content.append(tag)

                tag = soup.children.next()
                if isinstance(tag, Tag) and \
                        (self.incut_class in tag.attrs.get('class', '') or
                         self.content_class in tag.attrs.get('class', '')):
                    tag = None
        except StopIteration:
            pass

        if len(content):
            soup.append(content)

        return soup.decode()


class IncutExtenssion(Extension):
    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add(
            'incut', IncutProcessor(md), '_begin',
        )


def makeExtension(*args, **kwargs):
    return IncutExtenssion(*args, **kwargs)
