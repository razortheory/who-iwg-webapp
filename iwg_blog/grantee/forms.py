import copy

from ..blog.fields import MarkdownFormField
from ..blog.forms import ArticleAdminForm
from ..blog.widgets import CustomMarkdownWidget


class GranteeAdminForm(ArticleAdminForm):
    autosave_prefix = 'blog_grantee'

    class Meta(ArticleAdminForm.Meta):
        widgets = copy.deepcopy(ArticleAdminForm.Meta.widgets)
        widgets['short_description'] = CustomMarkdownWidget

        field_classes = copy.deepcopy(ArticleAdminForm.Meta.field_classes)
        field_classes['short_description'] = MarkdownFormField
