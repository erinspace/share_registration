from django import forms


class ProviderForm(forms.Form):
    provider_name = forms.CharField(max_length=50)
    base_url = forms.URLField()
    property_list = forms.CharField(widget=forms.Textarea)
    approved_sets = forms.CharField(widget=forms.Textarea)
