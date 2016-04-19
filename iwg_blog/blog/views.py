from meta.views import Meta

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.views.generic import DetailView, ListView, TemplateView

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


class ArticlePreviewView(ArticleView):
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(ArticlePreviewView, self).get_object()
        obj.content = self.request.POST.get('data', 'No content posted')
        return obj


class ArticleListView(BaseViewMixin, ListView):
    model = Article
    queryset = Article.objects.all()

    template_name = 'article_list.html'

    def get_meta_context(self):
        return Meta(title='Article list',
                    description='List of articles.',
                    url=reverse('articles_view')
                    )


class SearchView(BaseViewMixin, ListView):
    model = Article

    template_name = 'article_list.html'

    def get_queryset(self):
        search_string = self.request.GET.get('q', '')
        return self.model.objects.filter(title__icontains=search_string)

    def get_meta_context(self):
        url = reverse('search_view') + '?' + self.request.GET.urlencode()
        return Meta(title='Search result',
                    description='Search result.',
                    url=url
                    )


class LandingView(BaseViewMixin, TemplateView):
    template_name = 'landing.html'

    def get_meta_context(self):
        return Meta(title='IWG Portal',
                    description='IWG Portal',
                    url=reverse('landing_view'),
                    )

