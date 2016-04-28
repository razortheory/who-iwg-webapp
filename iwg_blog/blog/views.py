from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db import models
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import DetailView, ListView, CreateView, UpdateView

from meta.views import Meta
from watson import search as watson

from iwg_blog.attachments.views import FeaturedDocumentsMixin
from .forms import SubscribeForm, UnsubscribeForm
from .models import Article, Subscriber, Tag, Category


class BaseViewMixin(object):
    def get_meta_context(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        context['scheme'] = settings.META_SITE_PROTOCOL

        context['meta'] = self.get_meta_context()

        return context


class CategoriesMixin(object):
    def get_context_data(self, **kwargs):
        context = dict()
        context['categories'] = Category.objects.all()
        context.update(kwargs)
        return super(CategoriesMixin, self).get_context_data(**context)


class FeaturedArticlesMixin(object):
    featured_articles_count = 2

    def get_context_data(self, **kwargs):
        context = dict()
        context['featured_articles'] = Article.published.filter(is_featured=True)[:self.featured_articles_count]
        context.update(kwargs)
        return super(FeaturedArticlesMixin, self).get_context_data(**context)


class TopArticlesMixin(object):
    top_articles_count = 3

    def get_context_data(self, **kwargs):
        context = dict()
        context['top_articles'] = Article.published.order_by('-hits')[:self.top_articles_count]
        context.update(kwargs)
        return super(TopArticlesMixin, self).get_context_data(**context)


class TopTagsMixin(object):
    top_tags_count = 10

    def get_context_data(self, **kwargs):
        context = dict()
        context['top_tags'] = Tag.objects.annotate(article_count=models.Count('articles')) \
            .order_by('-article_count')[:self.top_tags_count]
        context.update(kwargs)
        return super(TopTagsMixin, self).get_context_data(**context)


class RelatedListMixin(MultipleObjectMixin, SingleObjectMixin):
    object_queryset = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(self.object_queryset)
        return super(RelatedListMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RelatedListMixin, self).get_context_data(**kwargs)
        context_object_name = SingleObjectMixin.get_context_object_name(self, self.object)
        context[context_object_name] = self.object
        return context


class ArticleView(BaseViewMixin, DetailView):
    model = Article
    queryset = Article.published.all()
    template_name = 'pages/article.html'

    related_articles_count = 3

    def get_meta_context(self):
        return self.get_object().as_meta(self.request)

    def get_context_data(self, **kwargs):
        context = dict()
        context['related_articles'] = self.get_queryset().exclude(pk=self.object.pk) \
            .filter(category=self.object.category)[:self.related_articles_count]
        context.update(kwargs)
        return super(ArticleView, self).get_context_data(**context)


class ArticlePreviewView(AccessMixin, ArticleView):
    queryset = Article.objects.all()

    raise_exception = True
    permission_required = ['blog.add_article', 'blog.add_samplearticle', 'blog.add_samplearticle',
                           'blog.change_article_slug', 'blog.change_samplearticle']

    def has_permission(self):
        if not self.request.user.is_staff:
            return False

        for permission in self.permission_required:
            if self.request.user.has_perm(permission, self.object):
                return True

        return False

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.has_permission():
            return self.handle_no_permission()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = super(ArticlePreviewView, self).get_object()
        obj.content = self.request.POST.get('data', 'No content posted')
        return obj


class ArticleListView(BaseViewMixin, ListView):
    model = Article
    queryset = Article.published.all()

    def get_meta_context(self):
        return Meta(title='Article list',
                    description='List of articles.',
                    url=reverse('blog:articles_view')
                    )


class SearchView(ArticleListView):
    search_string = None

    template_name = 'pages/search-page.html'

    def get(self, request, *args, **kwargs):
        self.search_string = self.request.GET.get('q', '')
        return super(SearchView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()

        if not self.search_string:
            return queryset

        return watson.filter(self.queryset, self.search_string, ranking=True)

    def get_context_data(self, **kwargs):
        context = dict()
        context['search_string'] = self.search_string
        context.update(kwargs)
        return super(SearchView, self).get_context_data(**context)

    def get_meta_context(self):
        url = reverse('blog:search_view') + '?' + self.request.GET.urlencode()
        return Meta(title='Search result',
                    description='Search result.',
                    url=url
                    )


class LandingView(FeaturedArticlesMixin, TopArticlesMixin, TopTagsMixin,
                  FeaturedDocumentsMixin, CategoriesMixin, ArticleListView):
    template_name = 'pages/index.html'

    def get_meta_context(self):
        return Meta(title='IWG Portal',
                    description='IWG Portal',
                    url=reverse('blog:landing_view'),
                    )


class CategoryView(RelatedListMixin, ArticleListView):
    template_name = 'pages/category-page.html'
    object_queryset = Category.objects.all()

    def get_queryset(self):
        return super(CategoryView, self).get_queryset().filter(category=self.object)


class TagView(RelatedListMixin, ArticleListView):
    template_name = 'pages/tagged-page.html'
    object_queryset = Tag.objects.all()

    def get_queryset(self):
        return super(TagView, self).get_queryset().filter(tags=self.object)


class SubscribeForUpdates(CreateView):
    model = Subscriber
    form_class = SubscribeForm
    template_name = 'subscribe_form.html'
    success_url = reverse_lazy('blog:landing_view')


class UnsubscribeFromUpdates(UpdateView):
    model = Subscriber
    form_class = UnsubscribeForm
    template_name = 'subscribe_form.html'
    success_url = reverse_lazy('blog:landing_view')

    def get_object(self, queryset=None):
        if self.request.method in ('POST', 'PUT'):
            email = self.request.POST.get('email')
            return Subscriber.objects.filter(email=email).first()
        return None