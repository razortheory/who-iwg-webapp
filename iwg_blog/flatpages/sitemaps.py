from django.contrib.flatpages.sitemaps import FlatPageSitemap


class PriorityFlatPageSitemap(FlatPageSitemap):
    priority = 0.5
