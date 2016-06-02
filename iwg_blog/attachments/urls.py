from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^ajax/upload-image/$', views.UploadImageAjaxView.as_view(), name='upload_image_ajax'),
]
