from django import forms

class ReportForm(forms.Form):
    message = forms.CharField(label='Bitte beschreibe warum du den Post melden möchtest.', max_length=1000)
