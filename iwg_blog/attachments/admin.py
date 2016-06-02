from django.contrib import admin

from .models import Document, Link, UploadedImage


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured', 'document_preview')
    list_filter = ('is_featured', )
    search_fields = ('name',)
    readonly_fields = ('document_preview', )
    exclude = ('file_preview', )
    list_per_page = 20

    def document_preview(self, obj):
        return '<img class="document-preview" src="%s">' % obj.get_preview_url()
    document_preview.allow_tags = True
    document_preview.short_description = 'Preview'


class DocumentAdminInline(admin.TabularInline):
    exclude = ['is_featured', 'file_preview']
    readonly_fields = ['document_preview_thumb', ]

    def document_preview_thumb(self, obj):
        return '<img class="document-preview" width="100" src="%s">' % obj.file_preview.url if obj.file_preview else ''
    document_preview_thumb.short_description = 'Preview'
    document_preview_thumb.allow_tags = True


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'image_url')

    def image_preview(self, obj):
        return '<img height="50" src="%s">' % obj.image_file.url
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

    def image_url(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.image_file.url)
    image_url.allow_tags = True


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
