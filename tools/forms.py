from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg"}))


class ToolErrorForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "cols": 80,
                "rows": 4,
                "placeholder": _("What error are your facing?"),
                "class": "form-control",
            }
        ),
    )

    def send_mail(self):
        cd = self.cleaned_data
        tool = self.tool

        subject = f"Error reported for {tool.name}"
        message = f"Name:{cd['name']}\nEmail:{cd['email']}\nSlug:{tool.get_absolute_url()}\nMessage:{cd['message']}"

        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_TO_EMAIL],
        )
