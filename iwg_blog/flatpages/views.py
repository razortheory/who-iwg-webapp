from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import DEFAULT_TEMPLATE
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import Http404, HttpResponsePermanentRedirect
from django.utils.safestring import mark_safe
from django.views.generic.detail import DetailView

from meta.views import MetadataMixin

from ..blog.helpers import Meta


class FlatPageView(MetadataMixin, DetailView):
    meta_class = Meta
    model = FlatPage

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        url = self.kwargs['url']

        if not url.startswith('/'):
            url = '/' + url
        site_id = get_current_site(self.request).id
        f = queryset.filter(url=url, sites=site_id).first()
        if not f:
            if not url.endswith('/') and settings.APPEND_SLASH:
                url += '/'
                f = queryset.filter(url=url, sites=site_id).first()
        return f

    def get_meta_title(self, context={}):
        return self.object.title

    def get_context_data(self, **kwargs):
        context = super(FlatPageView, self).get_context_data(**kwargs)
        context['flatpage'] = self.object
        return context

    def get_template_names(self):
        return [obj for obj in [self.object.template_name, DEFAULT_TEMPLATE] if obj]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            raise Http404

        self.object.title = mark_safe(self.object.title)
        self.object.content = mark_safe(self.object.content)

        if not self.kwargs['url'] and settings.APPEND_SLASH:
            return HttpResponsePermanentRedirect('%s/' % self.request.path)

        if self.object.registration_required and not request.user.is_authenticated():
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.path)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
