class DictSerializer(object):
    """
    Dict serializer for objects. Fetch all fields, notated in serializable_fields from obj and return as data
    """
    serializable_fields = []

    def __init__(self, *args, **kwargs):
        if 'serializable_fields' in kwargs:
            self.serializable_fields = kwargs.pop('serializable_fields')

    def serialize_obj(self, obj):
        data = {}
        for field in self.serializable_fields:
            if hasattr(self, 'serialize_%s' % field):
                data[field] = getattr(self, 'serialize_%s' % field)(getattr(obj, field))
            else:
                data[field] = getattr(obj, field)

            if callable(data[field]):
                data[field] = data[field]()
        return data

    def serialize(self, obj, many=False):
        if many:
            data = {
                'data': [self.serialize_obj(single_obj) for single_obj in obj],
            }
        else:
            data = self.serialize_obj(obj)

        return data
