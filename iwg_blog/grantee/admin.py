from django.contrib import admin

from .models import Grantee


@admin.register(Grantee)
class GranteeAdmin(admin.ModelAdmin):
    list_display = ('name', )
