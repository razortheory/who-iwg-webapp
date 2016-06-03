import copy

from django.contrib import admin, messages
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.encoding import force_text

from watson.search import default_search_engine

from ..attachments.admin import DocumentAdminInline
from ..utils.admin import ConfigurableModelAdmin, remove_from_fieldsets
from ..utils.base import update_url_params
from .forms import ArticleAdminForm, FlatPagesAdminForm
from .models import Article, ArticleDocument, BaseArticle, Category, SampleArticle, Subscriber, Tag
from .watson_adapters import ArticleAdapter


class ArticleDocumentInline(DocumentAdminInline):
    model = ArticleDocument


class BaseArticleAdmin(ConfigurableModelAdmin):
    form = ArticleAdminForm
    change_form_template = 'admin/custom_change_form.html'

    fieldsets = (
        (None, {'fields': ['title', 'slug', 'status', 'published_at']}),
        (None, {'fields': ['cover_image', 'short_description', 'content']}),
    )

    _status_colors = {
        BaseArticle.STATUS_PUBLISHED: '#008000',
        BaseArticle.STATUS_READY_FOR_PUBLISH: '#0079FF',
        BaseArticle.STATUS_DRAFT: '#717171',
    }

    def change_status(self, request, queryset, status):
        model = queryset.model
        opts = model._meta

        status_display = force_text(dict(opts.get_field('status').flatchoices).get(status, status), strings_only=True)
        objects_count = queryset.count()

        update_fields = {'status': status}
        if status == model.STATUS_PUBLISHED:
            update_fields['published_at'] = models.Case(models.When(~models.Q(status=model.STATUS_PUBLISHED),
                                                                    then=timezone.now()),
                                                        default=models.F('published_at'))
        queryset.update(**update_fields)
        messages.success(request, 'Status set to "%s" in %s %s.' % (
            status_display, objects_count, opts.verbose_name if objects_count == 1 else opts.verbose_name_plural
        ))
    change_status.short_description = 'Mark as "%(status_name)s"'

    def colorized_status(self, obj):
        color = self._status_colors[obj.status]
        return '<strong style="color: %s">%s</strong>' % (color, obj.get_status_display())
    colorized_status.short_description = 'Status'
    colorized_status.admin_order_field = 'status'
    colorized_status.allow_tags = True

    def make_action(self, action, kwargs, context):
        if callable(action):
            func = action
            action = action.__name__

        elif hasattr(self.__class__, action):
            func = getattr(self.__class__, action)

        description = func.short_description % context
        action += '__' + '__'.join(map(lambda x: '%s__%s' % x, kwargs.items()))
        return lambda s, r, q: func(s, r, q, **kwargs), action, description

    def get_actions(self, request):
        actions = super(BaseArticleAdmin, self).get_actions(request)

        for value, name in BaseArticle.CHOICES_STATUS:
            action = self.make_action('change_status', {'status': value}, {'status_name': name})
            actions[action[1]] = action

        return actions

    def list_display_hits(self, request):
        return request.user.has_perm('blog.view_article_hits')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(BaseArticleAdmin, self).get_readonly_fields(request, obj=obj)[:]
        if obj:
            readonly_fields += ('slug', )
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(BaseArticleAdmin, self).get_fieldsets(request, obj=obj))
        if not obj:
            remove_from_fieldsets(fieldsets, 'published_at')
        return fieldsets


@admin.register(Article)
class ArticleAdmin(BaseArticleAdmin):
    list_display = [
        'title', 'category', 'tags_list', 'short_description',
        'published_at', 'is_featured', 'colorized_status', 'hits', 'words_count'
    ]
    list_filter = ['is_featured', 'status', 'category', 'published_at']

    fieldsets = copy.deepcopy(BaseArticleAdmin.fieldsets)
    fieldsets[0][1]['fields'].insert(2, 'tags')
    fieldsets[0][1]['fields'].insert(2, 'category')
    fieldsets[0][1]['fields'] += ['is_featured']

    search_adapter_cls = ArticleAdapter
    search_engine = default_search_engine
    # Dirty hack for displaying search input
    search_fields = [None]

    inlines = (ArticleDocumentInline,)

    actions = ['mark_featured', 'unmark_featured']

    def mark_featured(self, request, queryset):
        model = queryset.model
        opts = model._meta

        objects_count = queryset.count()

        queryset.update(is_featured=True)
        messages.success(request, '%s %s marked as featured.' % (
            objects_count, opts.verbose_name if objects_count == 1 else opts.verbose_name_plural
        ))
    mark_featured.short_description = 'Mark as featured'

    def unmark_featured(self, request, queryset):
        model = queryset.model
        opts = model._meta

        objects_count = queryset.count()

        queryset.update(is_featured=False)
        messages.success(request, 'Featured flag removed from %s %s.' % (
            objects_count, opts.verbose_name if objects_count == 1 else opts.verbose_name_plural
        ))
    unmark_featured.short_description = 'Remove featured flag'

    def get_queryset(self, request):
        return super(ArticleAdmin, self).get_queryset(request).prefetch_related('category')

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False

        return self.search_engine.filter(queryset, search_term, ranking=False), False

    def changelist_view(self, request, extra_context=None):
        # Dirty hack for tags
        self.request = request
        return super(ArticleAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['tags'].widget.can_add_related = False
        return form

    def tags_list(self, obj):
        return ', '.join([
            u'<a href="%s">%s</a>' % (
                update_url_params(self.request.get_full_path(), {'tags__id__exact': tag.id}), tag
            ) for tag in obj.tags.all()
        ])
    tags_list.short_description = 'Tags'
    tags_list.allow_tags = True


@admin.register(SampleArticle)
class SampleArticleAdmin(ArticleAdmin):
    new_article_action_name = '_create_article'

    def render_change_form(self, request, context, **kwargs):
        if kwargs.get('obj'):
            context = context or {}
            context.update({
                'additional_actions': [
                    {'text': 'Create new article from sample', 'name': self.new_article_action_name}
                ]
            })
        return super(SampleArticleAdmin, self).render_change_form(request, context, **kwargs)

    def response_change(self, request, obj):
        if self.new_article_action_name in request.POST:
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

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SampleArticleAdmin, self).get_fieldsets(request, obj)
        remove_from_fieldsets(fieldsets, ['status', 'published_at', 'is_featured'])
        return fieldsets


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'article_count')

    def get_queryset(self, request):
        return super(TagAdmin, self).get_queryset(request) \
            .extra(select={'article_count': """
                SELECT COUNT(1) FROM blog_article_tags as ET1
                                    INNER JOIN blog_article as ET2 ON ET1.article_id = ET2.id
                                                                       AND ET2.is_sample = false
                                    WHERE ET1.tag_id = blog_tag.id
            """})

    def article_count(self, obj):
        return obj.article_count
    article_count.short_description = 'Articles'
    article_count.admin_order_field = 'article_count'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'send_email')


admin.site.unregister(FlatPage)
@admin.register(FlatPage)
class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPagesAdminForm
    fields = ['url', 'title', 'content', 'registration_required', ]
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')

    def save_related(self, request, form, formsets, change):
        super(FlatPageAdmin, self).save_related(request, form, formsets, change)
        form.instance.sites.add(Site.objects.get_current(request))


admin.site.unregister(Site)
@admin.register(Site)
class SiteAdmin(SiteAdmin):
    def get_actions(self, request):
        actions = super(SiteAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
