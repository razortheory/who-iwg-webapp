from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Layout, Field

from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', ]

    def clean(self):
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']

        if Subscriber.objects.filter(email=email, send_email=True).exists():
            raise forms.ValidationError("You have already subscribed for updates.")

        return email

    def save(self, commit=True):
        try:
            self.instance = Subscriber.objects.get(email=self.instance.email)
            self.instance.send_email = True
        except Subscriber.DoesNotExist:
            pass
        return super(SubscribeForm, self).save(commit)


class UnsubscribeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'article__form'
        self.helper.layout = Layout(
            Field('send_email', type="hidden"),
            ButtonHolder(
                Submit('submit', 'Unsubscribe', css_class='article__form__button button')
            )
        )

    def clean_send_email(self):
        return False

    class Meta:
        model = Subscriber
        fields = ['send_email', ]
