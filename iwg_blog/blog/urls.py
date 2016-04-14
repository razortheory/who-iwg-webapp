from django.conf.urls import url

from .views import ArticleView, ArticleListView, SearchView, LandingView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing_view'),
    url(r'^search/?$', SearchView.as_view(), name='search_view'),
    url(r'^articles/?$', ArticleListView.as_view(), name='articles_view'),
    url(r'^articles/(?P<pk>\d+)/?$', ArticleView.as_view(), name='article_detail_view'),
]