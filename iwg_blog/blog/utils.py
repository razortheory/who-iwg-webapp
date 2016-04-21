import urllib
import urlparse

from bs4 import BeautifulSoup
from markdown import markdown


def dict_merge(*args):
    dicts_list = []
    for dict_obj in args:
        dicts_list += (dict_obj or {}).items()
    return dict(dicts_list)


def update_url_params(url, params):
    url_parts = list(urlparse.urlparse(url))
    current_params = dict(urlparse.parse_qsl(url_parts[4]))
    url_parts[4] = urllib.urlencode(dict_merge(current_params, params))
    return urlparse.urlunparse(url_parts)


def markdown_to_text(markdown_text):
    return BeautifulSoup(markdown(markdown_text)).get_text()
