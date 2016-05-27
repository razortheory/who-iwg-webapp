from ..utils.serializers import DictSerializer


class UploadedImageSerializer(DictSerializer):
    serializable_fields = ['image_file', ]

    def serialize_image_file(self, value):
        return {
            'url': value.url,
            'width': value.width,
            'height': value.height,
        }
