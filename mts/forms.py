from django import forms


class LoadXMLForm(forms.Form):
    xml = forms.FileField(required=True)
