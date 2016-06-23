from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView

from meta.views import MetadataMixin
from watson import search as watson

from ...attachments.views import LinksMixin, FeaturedDocumentsMixin
from ...utils.views import HitsTrackingMixin, BaseViewMixin, JsonResponseMixin, RelatedListMixin
from ..forms import SubscribeForm, UnsubscribeForm
from ..helpers import Meta
from ..models import Article, BaseArticle, Category, Tag, Subscriber
from ..serializers import ArticleSerializer
from .mixins import FeaturedArticlesMixin, TopArticlesMixin, TopTagsMixin, CategoriesMixin


class ArticleView(MetadataMixin, HitsTrackingMixin, BaseViewMixin, DetailView):
    meta_class = Meta
    model = Article
    template_name = 'blog/pages/article.html'

    related_articles_count = 3

    def get_meta(self, **kwargs):
        return self.get_object().as_meta(self.request)

    def get_context_data(self, **kwargs):
        context = dict()
        related_articles = self.get_queryset() \
                               .filter(status=BaseArticle.STATUS_PUBLISHED, published_at__lte=timezone.now()) \
                               .exclude(pk=self.object.pk) \
                               .filter(categories__in=self.object.categories.all())[:self.related_articles_count]
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
    paginate_by = 6

    def get_queryset(self):
        return Article.published.all()

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

        return watson.filter(queryset, self.search_string, ranking=True)

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
    object_model = Category
    paginate_by = 12

    def get_queryset(self):
        return super(CategoryView, self).get_queryset().filter(categories=self.object)

    def get_meta(self, **context):
        return self.object.as_meta(self.request)


class TagView(RelatedListMixin, ArticleListView):
    template_name = 'blog/pages/tagged-page.html'
    object_model = Tag

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
    template_name = 'blog/pages/unsubscribe_form.html'
    success_url = reverse_lazy('blog:landing_view')

    def get_email(self):
        return self.kwargs['email']

    def get_initial(self):
        initial = super(UnsubscribeFromUpdates, self).get_initial()
        initial['email'] = self.get_email()
        return initial

    def get_object(self, queryset=None):
        return Subscriber.objects.filter(email=self.get_email(), email__isnull=False).first()
