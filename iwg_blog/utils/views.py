from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import QuerySet
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .serializers import DictSerializer


class JsonResponseMixin(object):
    """
    Django CBV mixin for using ajax requests without any heavy libraries
    """
    serializer_class = DictSerializer

    def get_serializer(self):
        return self.serializer_class()

    def serialize(self, obj):
        if isinstance(obj, (list, tuple, QuerySet)):
            return self.get_serializer().serialize(obj, many=True)
        return self.get_serializer().serialize(obj)


class BaseViewMixin(object):
    """
    Add domain info to context.
    """
    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        context['scheme'] = settings.META_SITE_PROTOCOL

        return context


class RelatedListMixin(MultipleObjectMixin, SingleObjectMixin):
    """
    A base view mixin for displaying a list of related objects.
    """
    object_queryset = None
    object_model = None

    def get_object_queryset(self):
        if self.object_queryset is not None:
            return self.object_queryset.all()

        if self.object_model:
            return self.object_model._default_manager.all()

        raise ImproperlyConfigured(
            "%(cls)s is missing a object QuerySet. Define "
            "%(cls)s.object_model, %(cls)s.object_queryset, or override "
            "%(cls)s.get_object_queryset()." % {
                'cls': self.__class__.__name__
            }
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(self.get_object_queryset())
        return super(RelatedListMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RelatedListMixin, self).get_context_data(**kwargs)
        context_object_name = SingleObjectMixin.get_context_object_name(self, self.object)
        context[context_object_name] = self.object
        return context


class HitsTrackingMixin(object):
    """
    View mixin for tracking hits.
    """
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
