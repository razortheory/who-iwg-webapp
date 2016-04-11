from django.contrib import admin

from .forms import ArticleAdminForm
from .models import Article, Category, Tag
from ..attachments.admin import DocumentAdminInline


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', )
    search_fields = ('title', )
    inlines = (DocumentAdminInline, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
