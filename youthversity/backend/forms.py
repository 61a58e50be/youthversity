from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Subject, ViolationReport


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, required=True, help_text='Required')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class ReportForm(forms.Form):
    message = forms.CharField(
        label='Bitte beschreibe warum du den Post melden möchtest.', max_length=3000, widget=forms.Textarea)

    class Meta:
        model = ViolationReport
        fields = (
            "content",
        )


class CommentCreationForm(forms.Form):
    content = forms.CharField(label='Dein Kommentar',
                              max_length=3000, widget=forms.Textarea)


class ProjectForm(forms.Form):
    title = forms.CharField(label='Titel', max_length=100)

    subjectChoices = [("Naturwissenschaften",
                      (("2", "Physik"),
                          ("3", "Chemie"),
                          ("4", "Mathe"),
                          ("5", "Biologie"),
                          ("6", "Sonstige"))),
                      ("Sprachen",
                      (("8", "Englisch"),
                          ("9", "Deutsch"),
                          ("10", "Französisch"),
                          ("11", "Spanisch"),
                          ("12", "Latein"),
                          ("13", "Altgriechisch"),
                          ("14", "Sonstige"))),
                      ("Gesellschaft",
                      (("16", "Geschichte"),
                          ("17", "Politik"),
                          ("18", "Wirtschaft"),
                          ("19", "Geographie"),
                          ("20", "Sozialkunde"),
                          ("21", "Sonstige"))),
                      ("Geisteswissenschaften",
                      (("23", "Philosophie"),
                          ("24", "Religion"))),
                      ("Technik",
                      (("26", "Informatik"),
                       ("27", "Sonstige"))),
                      ("28", "Musik"),
                      ("29", "Kunst"),
                      ("30", "Sport"),
                      ("31", "Sonstige")]

    subject = forms.CharField(
        label='Thema', widget=forms.Select(choices=subjectChoices))
    content = forms.CharField(widget=CKEditorUploadingWidget())
    file = forms.FileField(required=False)
    check = forms.BooleanField(label="Ich versichere, dass alle Inhalte mein geistiges Eigentum sind oder mit "
                                     + "Erlaubnis des Erstellers verwendet werden und Quellen korrekt zitiert wurden")

    class Meta:
        model = Post
        fields = (
            "title",
            "subject",
            "content",
            "file",
        )


class ReportCheckForm(forms.Form):
    answer = forms.CharField(max_length=2000, label='answer')
    violation = forms.BooleanField(label='violation')
