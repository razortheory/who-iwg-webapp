from django.http import JsonResponse
from django.views.generic import CreateView

from ..utils.views import JsonResponseMixin
from .forms import UploadImageForm
from .models import Document, UploadedImage, Link
from .serializers import UploadedImageSerializer


class FeaturedDocumentsMixin(object):
    featured_documents_count = 3

    def get_context_data(self, **kwargs):
        context = dict()
        context['featured_documents'] = Document.objects.filter(is_featured=True)[:self.featured_documents_count]
        context.update(kwargs)
        return super(FeaturedDocumentsMixin, self).get_context_data(**context)


class UploadImageAjaxView(JsonResponseMixin, CreateView):
    form_class = UploadImageForm
    model = UploadedImage
    serializer_class = UploadedImageSerializer

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse(self.serialize(obj))


class LinksMixin(object):
    def get_context_data(self, **kwargs):
        context = dict()
        context['links'] = Link.objects.all()[:10]
        context.update(kwargs)
        return super(LinksMixin, self).get_context_data(**context)


