from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

from .forms import FlatPagesAdminForm


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPagesAdminForm
    fields = ['url', 'title', 'content', 'registration_required', ]
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')

    def save_related(self, request, form, formsets, change):
        super(FlatPageAdmin, self).save_related(request, form, formsets, change)
        form.instance.sites.add(Site.objects.get_current(request))
