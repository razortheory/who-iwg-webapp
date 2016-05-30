import base64
import math
import six
import urllib
from io import BytesIO

from PIL import Image, ImageEnhance, ImageStat
from sorl.thumbnail import default
from sorl.thumbnail.engines.pil_engine import Engine


class WatermarkMixin(object):
    def create(self, image, geometry, options):
        image = super(WatermarkMixin, self).create(image, geometry, options)
        image = self.watermark(image, geometry, options)
        return image

    def watermark(self, image, geometry, options):
        watermark = options.get('watermark')
        if not watermark:
            return image

        return self._watermark(image, **watermark)

    def _watermark(self, image, *kwargs):
        raise NotImplementedError


def image_brightness(image):
    stat = ImageStat.Stat(image.convert('RGB'))
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


def parse_value(value, origin=None, context=None):
    if not isinstance(value, six.string_types):
        return value

    context = context or {}
    if origin:
        context['%'] = origin

    if value[-1] in ['%', 'w', 'h']:
        return context[value[-1]] * int(value[:-1]) / 100

    return int(value)


class ThumbnailEngine(WatermarkMixin, Engine):
    def _watermark(
        self, image, url=None,
        width=None, height=None, gravity=None, x=0, y=0,
        color=None, opacity=None, brightness_threshold=125
    ):
        if not url:
            raise ValueError('Watermark url is missing')

        watermark_key = 'watermark | %s' % url

        watermark_content_base64 = default.kvstore._get(watermark_key, identity='text')
        if watermark_content_base64 is None:
            watermark_content_base64 = base64.b64encode(urllib.urlopen(url).read())
            default.kvstore._set(watermark_key, watermark_content_base64, identity='text')

        watermark = Image.open(BytesIO(base64.b64decode(watermark_content_base64)))

        value_context = {'w': image.width, 'h': image.height}
        width = parse_value(width, image.width, value_context)
        height = parse_value(height, image.height, value_context)
        if width or height:
            if not width:
                width = watermark.width*height/watermark.height
            if not height:
                height = watermark.height*width/watermark.width
            watermark.thumbnail((width, height), resample=Image.ANTIALIAS)

        if x == 'center':
            x = (image.width - watermark.width) / 2
        if y == 'center':
            y = (image.height - watermark.height) / 2

        x = parse_value(x, image.width, value_context)
        y = parse_value(y, image.height, value_context)

        if gravity:
            if gravity[0] == 'b':
                y = image.height - watermark.height - y
            if gravity[1] == 'r':
                x = image.width - watermark.width - x

        if isinstance(color, (list, tuple)):
            brightness = image_brightness(image.crop((x, y, x + watermark.width, y + watermark.height)))
            if brightness < brightness_threshold:
                color = color[0]
            else:
                color = color[1]

        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        watermark_colored = Image.new('RGBA', watermark.size, color=color)
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark_colored.putalpha(alpha)
        image.paste(watermark_colored, (x, y), watermark_colored)

        return image
