from django.conf.urls import url

from . import views

app_name = 'grantee'

urlpatterns = [
    url(r'^grantees/$', views.GranteesView.as_view(), name='grantee_list_view'),
    url(r'^grantees/(?P<slug>[-a-zA-Z0-9_]+)/$', views.RoundView.as_view(), name='round_view'),
    url(r'^grantee/(?P<slug>[-a-zA-Z0-9_]+)/$', views.GranteeView.as_view(), name='grantee_view'),
]
