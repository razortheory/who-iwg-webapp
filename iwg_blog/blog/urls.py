from django.conf.urls import url

from .views import ArticleView, ArticleListView

urlpatterns = [
    url(r'^articles/?$', ArticleListView.as_view(), name='articles_view'),
    url(r'^articles/(?P<pk>\d+)/?$', ArticleView.as_view(), name='article_detail_view'),
]