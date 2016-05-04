from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps import Sitemap

from .models import Article


class ArticlesSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Article.objects.filter(status=Article.STATUS_PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class PriorityFlatPageSitemap(FlatPageSitemap):
    priority = 0.5
