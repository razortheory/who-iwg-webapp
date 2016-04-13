from django import forms

from .models import UploadedImage


class UploadImageForm(forms.ModelForm):
    class Meta:
        fields = forms.ALL_FIELDS
        model = UploadedImage
