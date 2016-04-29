from django.http import JsonResponse
from django.views.generic import CreateView

from .forms import UploadImageForm
from .models import UploadedImage, Document
from .serializers import JsonSerializer, UploadedImageSerializer


class FeaturedDocumentsMixin(object):
    featured_documents_count = 2

    def get_context_data(self, **kwargs):
        context = dict()
        context['featured_documents'] = Document.objects.filter(is_featured=True)[:self.featured_documents_count]
        context.update(kwargs)
        return super(FeaturedDocumentsMixin, self).get_context_data(**context)


class JsonResponseView(object):
    serializer_class = JsonSerializer

    def get_serializer(self):
        return self.serializer_class()

    def serialize(self, obj):
        return self.get_serializer().serialize(obj)


class UploadImageAjaxView(JsonResponseView, CreateView):
    form_class = UploadImageForm
    model = UploadedImage
    serializer_class = UploadedImageSerializer

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse(self.serialize(obj))
