from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
                      (("Physik", "Physik"),
                          ("Chemie", "Chemie"),
                          ("Mathe", "Mathe"),
                          ("Biologie", "Biologie"),
                          ("Sonstige", "Sonstige"))),
                      ("Sprachen",
                      (("Englisch", "Englisch"),
                          ("Deutsch", "Deutsch"),
                          ("Französisch", "Französisch"),
                          ("Spanisch", "Spanisch"),
                          ("Latein", "Latein"),
                          ("Altgriechisch", "Altgriechisch"),
                          ("Sonstige", "Sonstige"))),
                      ("Gesellschaft",
                      (("Geschichte", "Geschichte"),
                          ("Politik", "Politik"),
                          ("Wirtschaft", "Wirtschaft"),
                          ("Geographie", "Geographie"),
                          ("Sozialkunde", "Sozialkunde"),
                          ("Sonstige", "Sonstige"))),
                      ("Geisteswissenschaften",
                      (("Philosophie", "Philosophie"),
                          ("Religion", "Religion"))),
                      ("Technik",
                      (("Informatik", "Informatik"),
                       ("Sonstige", "Sonstige"))),
                      ("Musik", "Musik"),
                      ("Kunst", "Kunst"),
                      ("Sport", "Sport"),
                      ("Sonstige", "Sonstige")]

    subject = forms.CharField(
        label='Thema', widget=forms.Select(choices=subjectChoices))
    content = forms.CharField(label='Text', widget=forms.Textarea)
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
