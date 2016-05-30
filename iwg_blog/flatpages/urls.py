from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(.*)$', views.FlatPageView.as_view(), name='django.contrib.flatpages.views.flatpage'),
]
