from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.LandingView.as_view(), name='landing_view'),
    url(r'^search/?$', views.SearchView.as_view(), name='search_view'),
    url(r'^subscribe/?$', views.SubscribeForUpdates.as_view(), name='subscribe_view'),
    url(r'^unsubscribe/?$', views.UnsubscribeFromUpdates.as_view(), name='unsubscribe_view'),
    url(r'^articles/?$', views.ArticleListView.as_view(), name='articles_view'),
    url(r'^articles/(?P<pk>\d+)/?$', views.ArticleView.as_view(), name='article_detail_view'),
    url(r'^articles/(?P<pk>\d+)/preview/?$', views.ArticlePreviewView.as_view(), name='article_preview_view'),
]