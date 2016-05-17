from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from meta.views import Meta

from ..blog.views import BaseViewMixin, RelatedListMixin, HitsTrackingMixin
from .models import Grantee, Round


class RoundsMixin(object):
    def get_context_data(self, **kwargs):
        context = dict()
        context['rounds'] = Round.objects.all()
        context.update(kwargs)
        return super(RoundsMixin, self).get_context_data(**context)


class GranteeView(HitsTrackingMixin, BaseViewMixin, DetailView):
    model = Grantee
    queryset = Grantee.objects.all()
    template_name = 'grantee/pages/grantee.html'

    related_articles_count = 3

    def get_meta_context(self, **context):
        return self.get_object().as_meta(self.request)


class RoundView(RoundsMixin, RelatedListMixin, BaseViewMixin, ListView):
    model = Grantee
    queryset = Grantee.published.all()

    template_name = 'grantee/pages/grantee-list.html'
    object_queryset = Round.objects.all()

    paginate_by = 6

    def get_meta_context(self, **context):
        return Meta(title='Grantees: %s' % self.object.name,
                    description='List of grantees.',
                    url=reverse('blog:articles_view')
                    )

    def get_queryset(self):
        return super(RoundView, self).get_queryset().filter(round=self.object)


class GranteesView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return Round.objects.first().get_absolute_url()
