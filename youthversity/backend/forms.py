from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Not optional.')

    class Meta:
        model = User
        fields = (
            "username",
        )

class ReportForm(forms.Form):
    message = forms.CharField(label='Bitte beschreibe warum du den Post melden möchtest.', max_length=1000)

