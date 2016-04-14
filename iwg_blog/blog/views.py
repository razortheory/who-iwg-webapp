from meta.views import Meta

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.views.generic import DetailView, ListView

from .models import Article


class BaseViewMixin(object):
    def get_meta_context(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        context['scheme'] = settings.META_SITE_PROTOCOL

        context['meta'] = self.get_meta_context()

        return context


class ArticleView(BaseViewMixin, DetailView):
    model = Article
    template_name = 'article.html'

    def get_meta_context(self):
        return self.get_object().as_meta(self.request)


class ArticleListView(BaseViewMixin, ListView):
    model = Article
    queryset = Article.objects.all()

    template_name = 'article_list.html'

    def get_meta_context(self):
        return Meta(title='Article list',
                    description='List of articles.',
                    url=reverse('articles_view')
                    )
