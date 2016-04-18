from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upload_image/ajax/?', views.UploadImageAjaxView.as_view(), name='upload_image_ajax'),
]
