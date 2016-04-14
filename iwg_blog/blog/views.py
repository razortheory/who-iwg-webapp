from django.core.urlresolvers import reverse
from meta.views import Meta

from django.views.generic import DetailView, ListView

from .models import Article


class ArticleView(DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)

        return context


class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.all()

    template_name = 'article_list.html'

    def get_meta_data_for_seo(self):
        return Meta(title='Article list',
                    description='List of articles.',
                    url=reverse('articles_view')
                    )

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['meta'] = self.get_meta_data_for_seo()

        return context