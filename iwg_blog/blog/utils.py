from bs4 import BeautifulSoup
from markdown import markdown


def markdown_to_text(markdown_text):
    return BeautifulSoup(markdown(markdown_text), 'html.parser').get_text()
