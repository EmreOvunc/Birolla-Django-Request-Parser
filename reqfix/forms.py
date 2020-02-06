from django import forms

class SimpleForm(forms.Form):
    request = forms.CharField(widget=forms.Textarea, max_length=2000, min_length=20, required='False')