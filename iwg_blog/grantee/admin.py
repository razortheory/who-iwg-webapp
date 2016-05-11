import copy

from django.contrib import admin

from ..blog.admin import BaseArticleAdmin
from .forms import GranteeAdminForm
from .models import Grantee, Round


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Grantee)
class GranteeAdmin(BaseArticleAdmin):
    form = GranteeAdminForm

    list_display = [
        'title', 'round', 'tags_list', 'short_description_preview',
        'published_at', 'status', 'hits', 'words_count'
    ]
    list_filter = ['status', 'round', 'published_at']
    readonly_fields = []

    fieldsets = copy.deepcopy(BaseArticleAdmin.fieldsets)
    fieldsets[0][1]['fields'].insert(2, 'round')

    def get_queryset(self, request):
        return super(GranteeAdmin, self).get_queryset(request).prefetch_related('round')

    def short_description_preview(self, obj):
        return obj.short_description_text
    short_description_preview.short_description = 'Short description (text)'
