from django import forms

class QueryForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={'class':'small-input'}), initial='What should I eat?')
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class':'small-postal'}), initial='M5V 2H5')