from django import forms

from push_endpoint.models import Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['longname', 'url', 'favicon_image']
