from django.db.models import QuerySet

from iwg_blog.utils.serializers import JsonSerializer


class JsonResponseMixin(object):
    serializer_class = JsonSerializer

    def get_serializer(self):
        return self.serializer_class()

    def serialize(self, obj):
        if isinstance(obj, (list, tuple, QuerySet)):
            return self.get_serializer().serialize(obj, many=True)
        return self.get_serializer().serialize(obj)
