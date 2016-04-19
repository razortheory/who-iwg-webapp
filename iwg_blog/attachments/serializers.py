class JsonSerializer(object):
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
        return data

    def serialize(self, obj):
        if isinstance(obj, (list, set, tuple)):
            data = [self.serialize_obj(single_obj) for single_obj in obj]
        else:
            data = self.serialize_obj(obj)

        return data


class UploadedImageSerializer(JsonSerializer):
    serializable_fields = ['image_file', ]

    def serialize_image_file(self, value):
        return {
            'url': value.url,
            'width': value.width,
            'height': value.height,
        }
