from ..blog.fields import MarkdownFormField
from ..blog.widgets import CustomMarkdownWidget
from ..blog.forms import ArticleAdminForm


class GranteeAdminForm(ArticleAdminForm):
    class Meta(ArticleAdminForm.Meta):
        widgets = ArticleAdminForm.Meta.widgets
        widgets['short_description'] = CustomMarkdownWidget

        field_classes = ArticleAdminForm.Meta.field_classes
        field_classes['short_description'] = MarkdownFormField
