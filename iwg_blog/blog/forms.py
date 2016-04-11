from django import forms

from django_select2.forms import Select2MultipleWidget


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'tags': Select2MultipleWidget,
        }
