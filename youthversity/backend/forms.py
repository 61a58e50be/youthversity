from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ViolationReport, Subject, Post

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class ReportForm(forms.Form):
    message = forms.CharField(label='Bitte beschreibe warum du den Post melden möchtest.', max_length=1000)

    class Meta:
        model = ViolationReport
        fields = (
            "content",
        )


class CommentCreationForm(forms.Form):
    content = forms.CharField(label='Dein Kommentar', max_length=1000)


class ProjectForm(forms.Form):
    title = forms.CharField(label='Titel', max_length=100)
    subjectChoices = []
    for subject in Subject.objects.all():
        subjectChoices += [(subject.name, subject.name)]
    subject = forms.CharField(label='Thema', widget=forms.Select(choices=subjectChoices))
    content = forms.CharField(label='Text', widget=forms.Textarea)
    file = forms.FileField(required=False)
    
    class Meta:
        model = Post
        fields = (
            "title",
            "subject",
            "content",
        )