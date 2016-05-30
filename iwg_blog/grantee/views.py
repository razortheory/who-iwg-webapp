from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from meta.views import MetadataMixin

from ..blog.helpers import Meta
from ..blog.views import BaseViewMixin, HitsTrackingMixin, RelatedListMixin
from .models import Grantee, Round


class RoundsMixin(object):
    def get_context_data(self, **kwargs):
        context = dict()
        context['rounds'] = Round.objects.all()
        context.update(kwargs)
        return super(RoundsMixin, self).get_context_data(**context)


class GranteeView(MetadataMixin, HitsTrackingMixin, BaseViewMixin, DetailView):
    meta_class = Meta
    model = Grantee
    queryset = Grantee.objects.all()
    template_name = 'grantee/pages/grantee.html'

    related_articles_count = 3

    def get_meta(self, **context):
        return self.get_object().as_meta(self.request)


class RoundView(MetadataMixin, RoundsMixin, RelatedListMixin, BaseViewMixin, ListView):
    meta_class = Meta
    model = Grantee
    queryset = Grantee.published.all()

    template_name = 'grantee/pages/grantee-list.html'
    object_queryset = Round.objects.all()

    paginate_by = 6

    url = reverse_lazy('grantee:grantee_list_view')

    def get_meta_title(self, context=None):
        return 'Grantees: %s' % self.object.name

    def get_queryset(self):
        return super(RoundView, self).get_queryset().filter(round=self.object)


class GranteesView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return Round.objects.first().get_absolute_url()
