import copy

from ..blog.fields import MarkdownFormField
from ..blog.forms import BaseArticleAdminForm
from ..blog.widgets import CustomMarkdownWidget


class GranteeAdminForm(BaseArticleAdminForm):
    autosave_prefix = 'blog_grantee'

    class Meta(BaseArticleAdminForm.Meta):
        widgets = copy.deepcopy(BaseArticleAdminForm.Meta.widgets)
        widgets['short_description'] = CustomMarkdownWidget

        field_classes = copy.deepcopy(BaseArticleAdminForm.Meta.field_classes)
        field_classes['short_description'] = MarkdownFormField
