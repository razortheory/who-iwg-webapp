from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import DetailView, ListView, CreateView, UpdateView

from meta.views import Meta
from watson import search as watson

from iwg_blog.attachments.views import FeaturedDocumentsMixin
from iwg_blog.blog.serializers import ArticleSerializer
from iwg_blog.utils.views import JsonResponseMixin
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
    featured_articles_count = 5

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
    queryset = Article.objects.all()
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


class ArticlePreviewView(AccessMixin, TemplateView):
    template_name = 'pages/article-preview.html'
    raise_exception = True

    def has_permission(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        return {'content': self.request.POST.get('data', 'No content posted')}

    def post(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        context = self.get_context_data()
        return self.render_to_response(context)


class ArticleListView(BaseViewMixin, ListView):
    model = Article
    queryset = Article.published.all()
    paginate_by = 6

    template_name = 'pages/article-list.html'

    def get_meta_context(self):
        return Meta(title='Article list',
                    description='List of articles.',
                    url=reverse('blog:articles_view')
                    )


class SearchView(JsonResponseMixin, ArticleListView):
    search_string = None

    template_name = 'pages/search-page.html'

    serializer_class = ArticleSerializer
    ajax_search_result_count = 3

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

    def get_ajax(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()[:self.ajax_search_result_count]
        return JsonResponse(self.serialize(self.object_list))

    def get(self, request, *args, **kwargs):
        self.search_string = self.request.GET.get('q', '')

        if request.is_ajax():
            return self.get_ajax(request, *args, **kwargs)
        return super(SearchView, self).get(request, *args, **kwargs)


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
    paginate_by = 12

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

    def form_valid(self, form):
        messages.success(self.request, 'You\'re successfully subscribed.')
        return super(SubscribeForUpdates, self).form_valid(form)

    def form_invalid(self, form):
        for errorlist in form.errors.values():
            for error in errorlist:
                messages.error(self.request, error)

        next_url = self.request.META.get('HTTP_REFERER') or 'blog:landing_view'
        return redirect(next_url)


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


class GetArticleSlugAjax(View):
    def post(self, *args, **kwargs):
        return JsonResponse({
            'status': 'ok',
            'slug': Article.generate_slug(
                self.request.POST.get('title', ''),
                instance_pk=self.request.POST.get('instance_pk')
            )
        })
