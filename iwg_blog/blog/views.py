from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from meta.views import MetadataMixin
from watson import search as watson

from iwg_blog.attachments.models import Link
from ..attachments.views import FeaturedDocumentsMixin
from ..blog.serializers import ArticleSerializer
from ..utils.views import JsonResponseMixin
from .forms import SubscribeForm, UnsubscribeForm
from .helpers import Meta
from .models import Article, BaseArticle, Category, Subscriber, Tag


class BaseViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        context['scheme'] = settings.META_SITE_PROTOCOL

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
    top_tags_count = 20

    def get_context_data(self, **kwargs):
        context = dict()
        context['top_tags'] = Tag.objects.annotate(article_count=models.Count('articles')) \
            .order_by('-article_count')[:self.top_tags_count]
        context.update(kwargs)
        return super(TopTagsMixin, self).get_context_data(**context)


class LinksMixin(object):
    def get_context_data(self, **kwargs):
        context = dict()
        context['links'] = Link.objects.all()
        context.update(kwargs)
        return super(LinksMixin, self).get_context_data(**context)


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


class HitsTrackingMixin(object):
    def get_hit_flag_name(self, obj):
        opts = obj._meta
        return 'hit_%s_%s_%s' % (opts.app_label, opts.model_name, obj.slug)

    def set_hit(self, obj):
        obj.hits = models.F('hits') + 1
        obj.save()

        self.request.session[self.get_hit_flag_name(obj)] = True

    def has_hit(self, obj):
        return self.request.session.get(self.get_hit_flag_name(obj))

    def get_object(self, queryset=None):
        obj = super(HitsTrackingMixin, self).get_object(queryset)

        if obj.status == obj.STATUS_PUBLISHED and not self.has_hit(obj):
            self.set_hit(obj)

        return obj


class ArticleView(MetadataMixin, HitsTrackingMixin, BaseViewMixin, DetailView):
    meta_class = Meta
    model = Article
    queryset = Article.objects.all()
    template_name = 'blog/pages/article.html'

    related_articles_count = 3

    def get_meta(self, **kwargs):
        return self.get_object().as_meta(self.request)

    def get_context_data(self, **kwargs):
        context = dict()
        related_articles = self.get_queryset() \
                               .filter(status=BaseArticle.STATUS_PUBLISHED).exclude(pk=self.object.pk) \
                               .filter(category=self.object.category)[:self.related_articles_count]
        if not related_articles:
            related_articles = self.model.published.order_by('-hits')[:self.related_articles_count]
        context['related_articles'] = related_articles

        context.update(kwargs)
        return super(ArticleView, self).get_context_data(**context)


class ArticlePreviewView(AccessMixin, TemplateView):
    template_name = 'blog/pages/article-preview.html'
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


class ArticleListView(MetadataMixin, BaseViewMixin, ListView):
    meta_class = Meta
    model = Article
    queryset = Article.published.all()
    paginate_by = 6

    template_name = 'blog/pages/article-list.html'

    title = 'Latest articles'
    url = reverse_lazy('blog:articles_view')
    image_width = 800
    image_height = 420


class SearchView(JsonResponseMixin, ArticleListView):
    search_string = None

    template_name = 'blog/pages/search-page.html'

    serializer_class = ArticleSerializer
    ajax_search_result_count = 3

    title = 'Search'

    def get_meta_url(self, context=None):
        return reverse('blog:search_view') + '?' + self.request.GET.urlencode()

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

    def get_ajax(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()[:self.ajax_search_result_count]
        return JsonResponse(self.serialize(self.object_list))

    def get(self, request, *args, **kwargs):
        self.search_string = self.request.GET.get('q', '')

        if request.is_ajax():
            return self.get_ajax(request, *args, **kwargs)
        return super(SearchView, self).get(request, *args, **kwargs)


class LandingView(FeaturedArticlesMixin, TopArticlesMixin, TopTagsMixin, LinksMixin,
                  FeaturedDocumentsMixin, CategoriesMixin, ArticleListView):
    template_name = 'blog/pages/index.html'

    title = 'IWG Portal'
    url = reverse_lazy('blog:landing_view')


class CategoryView(RelatedListMixin, ArticleListView):
    template_name = 'blog/pages/category-page.html'
    object_queryset = Category.objects.all()
    paginate_by = 12

    def get_queryset(self):
        return super(CategoryView, self).get_queryset().filter(category=self.object)

    def get_meta(self, **context):
        return self.object.as_meta(self.request)


class TagView(RelatedListMixin, ArticleListView):
    template_name = 'blog/pages/tagged-page.html'
    object_queryset = Tag.objects.all()

    def get_queryset(self):
        return super(TagView, self).get_queryset().filter(tags=self.object)

    def get_meta(self, **context):
        return self.object.as_meta(self.request)


class SubscribeForUpdates(CreateView):
    model = Subscriber
    form_class = SubscribeForm
    template_name = 'blog/subscribe_form.html'
    success_url = reverse_lazy('blog:landing_view')

    success_message = 'You\'re successfully subscribed.'

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            return JsonResponse({'message': self.success_message})

        messages.success(self.request, self.success_message)
        return super(SubscribeForUpdates, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'errors': form.errors}, status=400)

        return super(SubscribeForUpdates, self).form_invalid(form)


class UnsubscribeFromUpdates(UpdateView):
    model = Subscriber
    form_class = UnsubscribeForm
    template_name = 'blog/subscribe_form.html'
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


class TagsAutocompleteAjax(View):
    tags_count = 10

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('term', '')
        exclude = request.GET.getlist('exclude')

        queryset = Tag.objects.filter(name__startswith=tag).exclude(name__in=exclude) \
            .annotate(article_count=models.Count('articles')).order_by('-article_count') \
            .values_list('name', flat=True)[:self.tags_count]

        return JsonResponse(list(queryset), safe=False)


def page_not_found(request):
    return render(
        request, 'blog/pages/404.html',
        {
            'related_articles': Article.published.all()[:6]
        }, status=404
    )


def server_error(request):
    return render(request, 'blog/pages/500.html', {})
