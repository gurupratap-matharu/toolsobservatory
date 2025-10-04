from django import forms
from django.core.mail import send_mail

from .models import Comment


class SearchForm(forms.Form):
    query = forms.CharField()


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_mail(self):
        cd = self.cleaned_data
        post = self.post
        post_url = self.post_url

        subject = f"{cd['name']} recommends you read {post.title}..."
        message = f"Read {post.title} at {post_url}\n\nComments: {cd['comments']}"

        return send_mail(subject=subject, message=message, from_email=cd["email"], recipient_list=[cd["to"]])


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
