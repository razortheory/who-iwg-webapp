from django.conf.urls import url

from .views import ArticleView

urlpatterns = [
    url(r'^articles/(?P<pk>\d+)/?$', ArticleView.as_view(), name='article_view'),
]