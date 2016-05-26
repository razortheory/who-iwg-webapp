"""iwg_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from iwg_blog.blog.sitemaps import ArticlesSitemap, PriorityFlatPageSitemap
from iwg_blog.blog import views as blog_views

sitemaps = {
    'articles': ArticlesSitemap,
    'flatpages': PriorityFlatPageSitemap,
}


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^cms/adminpanel/', admin.site.urls),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^select2/', include('django_select2.urls')),

    url(r'^attachments/', include('iwg_blog.attachments.urls')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots.txt$', TemplateView.as_view(
        template_name='robots_allow.txt',
        content_type='text/plain'), name='robots'),

    url(r'', include('iwg_blog.blog.urls')),
    url(r'', include('iwg_blog.grantee.urls')),
    url(r'^pages/', include('iwg_blog.flatpages.urls')),
]


if settings.NEWRELIC_AVAILABILITY_TEST_ACTIVE:
    urlpatterns.append(url('availability-test/', include('iwg_blog.availability_monitor.urls')))


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = blog_views.page_not_found
handler500 = blog_views.server_error
