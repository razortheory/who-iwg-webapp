import copy

from django.contrib import admin

from ..attachments.admin import DocumentAdminInline
from ..blog.admin import BaseArticleAdmin
from .forms import GranteeAdminForm
from .models import Grantee, GranteeDocument, Round


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', )


class GranteeDocumentInline(DocumentAdminInline):
    model = GranteeDocument


@admin.register(Grantee)
class GranteeAdmin(BaseArticleAdmin):
    form = GranteeAdminForm

    list_display = [
        'title', 'round', 'short_description_preview',
        'published_at', 'colorized_status', 'hits', 'words_count'
    ]
    list_filter = ['status', 'round', 'published_at']
    readonly_fields = []

    inlines = [GranteeDocumentInline,]

    fieldsets = copy.deepcopy(BaseArticleAdmin.fieldsets)
    fieldsets[0][1]['fields'].insert(2, 'round')

    def get_queryset(self, request):
        return super(GranteeAdmin, self).get_queryset(request).prefetch_related('round')

    def short_description_preview(self, obj):
        short_description_text = obj.short_description_text
        if len(short_description_text) <= 100:
            return obj.short_description_text
        else:
            return obj.short_description_text[:100] + u'\u2026'
    short_description_preview.short_description = 'Short description (text)'
