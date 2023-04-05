from django import forms


class SimpleForm(forms.Form):
    password = forms.CharField(max_length=100, required=True)
