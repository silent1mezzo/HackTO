from django import forms

class QueryForm(forms.Form):
    q = forms.CharField()
    postal_code = forms.CharField(initial='M5V 2H5')

