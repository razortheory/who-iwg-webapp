from django.db.models import QuerySet

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
