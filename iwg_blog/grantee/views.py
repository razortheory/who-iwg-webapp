from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from meta.views import MetadataMixin

from ..blog.helpers import Meta
from ..utils.views import BaseViewMixin, RelatedListMixin, HitsTrackingMixin
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
    template_name = 'grantee/pages/grantee.html'

    def get_meta(self, **context):
        return self.get_object().as_meta(self.request)


class RoundView(MetadataMixin, RoundsMixin, RelatedListMixin, BaseViewMixin, ListView):
    meta_class = Meta
    model = Grantee
    object_model = Round
    paginate_by = 6

    template_name = 'grantee/pages/grantee-list.html'
    url = reverse_lazy('grantee:grantee_list_view')

    def get_meta_title(self, context=None):
        return 'Grantees: %s' % self.object.name

    def get_queryset(self):
        return Grantee.published.filter(round=self.object)


class GranteesView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return Round.objects.first().get_absolute_url()
