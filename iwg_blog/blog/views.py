from django.views.generic import DetailView

from .models import Article


class ArticleView(DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)

        return context