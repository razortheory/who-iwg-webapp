from iwg_blog.utils.serializers import JsonSerializer


class UploadedImageSerializer(JsonSerializer):
    serializable_fields = ['image_file', ]

    def serialize_image_file(self, value):
        return {
            'url': value.url,
            'width': value.width,
            'height': value.height,
        }
