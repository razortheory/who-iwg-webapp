from django.contrib import admin

from .models import Document, UploadedImage


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class DocumentAdminInline(admin.StackedInline):
    model = Document


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'image_url')

    def image_preview(self, obj):
        return "<img height=\"50\" src=\"%s\">" % obj.image_file.url
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

    def image_url(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.image_file.url)
    image_url.allow_tags = True
