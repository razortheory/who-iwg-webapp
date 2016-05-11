from django.conf.urls import url

from .views import GranteeView, RoundView, GranteesView

app_name = 'grantee'

urlpatterns = [
    url(r'^grantees/$', GranteesView.as_view(), name='grantee_list_view'),
    url(r'^grantees/(?P<slug>[-a-zA-Z0-9_]+)/$', RoundView.as_view(), name='round_view'),
    url(r'^grantee/(?P<slug>[-a-zA-Z0-9_]+)/$', GranteeView.as_view(), name='grantee_view'),
]
