from django.http import JsonResponse
from django.views.generic import CreateView

from .forms import UploadImageForm
from .models import UploadedImage
from .serializers import JsonSerializer, UploadedImageSerializer


class JsonResponseObjectView(object):
    serializer_class = JsonSerializer

    def get_serializer(self):
        return self.serializer_class()

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse(self.get_serializer().serialize(obj))


class UploadImageAjaxView(JsonResponseObjectView, CreateView):
    form_class = UploadImageForm
    model = UploadedImage
    serializer_class = UploadedImageSerializer
