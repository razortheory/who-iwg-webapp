from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<url>.*)$', views.FlatPageView.as_view(), name='django.contrib.flatpages.views.flatpage'),
]
