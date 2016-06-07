from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site


admin.site.unregister(Site)


@admin.register(Site)
class SiteAdmin(SiteAdmin):
    def get_actions(self, request):
        actions = super(SiteAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
