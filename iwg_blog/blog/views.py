from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db import models
from django.http import JsonResponse
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
from .models import Article, Subscriber, Tag, Category, BaseArticle


class BaseViewMixin(object):
    def get_meta_context(self, **context):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        context['scheme'] = settings.META_SITE_PROTOCOL

        context['meta'] = self.get_meta_context(**context)

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


class ArticleView(HitsTrackingMixin, BaseViewMixin, DetailView):
    model = Article
    queryset = Article.objects.all()
    template_name = 'pages/article.html'

    related_articles_count = 3

    def get_meta_context(self, **context):
        return self.get_object().as_meta(self.request)

    def get_context_data(self, **kwargs):
        context = dict()
        context['related_articles'] = self.get_queryset() \
            .filter(status=BaseArticle.STATUS_PUBLISHED).exclude(pk=self.object.pk) \
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

    def get_meta_context(self, **context):
        objects = context['object_list']
        image_url = objects[0].cover_image.url if objects and objects[0].cover_image else None
        return Meta(
            title='IWG Portal',
            description='List of articles.',
            url=reverse('blog:articles_view'),
            image=image_url,
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

    def get_meta_context(self, **context):
        url = reverse('blog:search_view') + '?' + self.request.GET.urlencode()
        objects = context['object_list']
        image_url = objects[0].cover_image.url if objects and objects[0].cover_image else None
        return Meta(
            title='IWG Portal',
            description='Search result.',
            url=url,
            image=image_url,
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

    def get_meta_context(self, **context):
        article = context.get('featured_articles').first()
        image_url = getattr(article, 'cover_image_url', '')
        return Meta(
            title='IWG Portal',
            description='IWG Portal',
            url=reverse('blog:landing_view'),
            image=image_url
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


class TagsAutocompleteAjax(View):
    tags_count = 10

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('term', '')
        exclude = request.GET.getlist('exclude')

        queryset = Tag.objects.filter(name__startswith=tag).exclude(name__in=exclude) \
            .annotate(article_count=models.Count('articles')).order_by('-article_count') \
            .values_list('name', flat=True)[:self.tags_count]

        return JsonResponse(list(queryset), safe=False)
