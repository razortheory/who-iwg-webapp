from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text

from watson.search import default_search_engine

from .forms import ArticleAdminForm
from .models import Article, Category, SampleArticle, Tag, Subscriber
from .utils import update_url_params
from .adapters import ArticleAdapter
from ..attachments.admin import DocumentAdminInline


class ConfigurableModelAdmin(admin.ModelAdmin):
    def _filter_configurable_list(self, request, configurable_list, prefix):
        for filter_attr in configurable_list:
            filter_func_name = prefix + filter_attr
            if hasattr(self, filter_func_name) and not getattr(self, filter_func_name)(request):
                configurable_list.remove(filter_attr)
        return configurable_list

    def get_list_filter(self, request):
        list_filter = super(ConfigurableModelAdmin, self).get_list_filter(request)[:]
        return self._filter_configurable_list(request, list_filter, 'list_filter_')

    def get_list_display(self, request):
        list_display = super(ConfigurableModelAdmin, self).get_list_display(request)[:]
        return self._filter_configurable_list(request, list_display, 'list_display_')


@admin.register(Article)
class ArticleAdmin(ConfigurableModelAdmin):
    form = ArticleAdminForm

    list_display = [
        'title', 'category', 'tags_list', 'short_description_preview',
        'published_at', 'is_featured', 'status', 'hits', 'words_count'
    ]
    list_filter = ['is_featured', 'status', 'category', 'published_at']
    inlines = (DocumentAdminInline, )
    readonly_fields = []

    search_adapter_cls = ArticleAdapter
    search_engine = default_search_engine
    search_fields = [None]

    def list_display_hits(self, request):
        return request.user.has_perm('blog.view_article_hits')

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super(ArticleAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        return super(ArticleAdmin, self).get_queryset(request).prefetch_related('category')

    def get_fields(self, request, obj=None):
        fields = super(ArticleAdmin, self).get_fields(request, obj=obj)[:]
        if obj:
            fields.remove('slug')
        return fields

    def short_description_preview(self, obj):
        return obj.short_description_text
    short_description_preview.short_description = 'Short description (text)'

    def tags_list(self, obj):
        return ', '.join([
             u'<a href="%s">%s</a>' % (
                 update_url_params(self.request.get_full_path(), {'tags__id__exact': tag.id}), tag
             ) for tag in obj.tags.all()
        ])
    tags_list.short_description = 'Tags'
    tags_list.allow_tags = True

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False

        return self.search_engine.filter(queryset, search_term, ranking=False), False


@admin.register(SampleArticle)
class SampleArticleAdmin(ArticleAdmin):
    def render_change_form(self, request, context, **kwargs):
        if kwargs.get('obj'):
            context = context or {}
            context.update({
                'additional_actions': [
                    {'text': 'Create new article from sample', 'name': '_create_article'}
                ]
            })
        return super(SampleArticleAdmin, self).render_change_form(request, context, **kwargs)

    def response_change(self, request, obj):
        if "_create_article" in request.POST:
            article = Article(sample=obj)
            article.save()
            article.tags.add(*obj.tags.all())

            msg = 'New article was created from "%(obj)s" successfully.' % {'obj': force_text(obj)}
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_change' % (self.model._meta.app_label, 'article'),
                                   current_app=self.admin_site.name, args=[article.pk])
            return HttpResponseRedirect(redirect_url)

        else:
            return super(SampleArticleAdmin, self).response_change(request, obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'send_email')
