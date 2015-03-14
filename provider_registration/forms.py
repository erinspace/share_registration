from django import forms
from django.forms import ModelForm

from provider_registration.models import RegistrationInfo


YES_NO_CHOICES = (
    (True, 'yes'),
    (False, 'no')
)


class InitialProviderForm(ModelForm):
    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'description',
                  'oai_provider', 'meta_tos', 'meta_privacy', 'meta_sharing_tos',
                  'meta_license', 'meta_license_extended', 'meta_future_license',
                  'contact_name', 'contact_email']


class OAIProviderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(OAIProviderForm, self).__init__(*args, **kwargs)
        self.fields['approved_sets'].choices = self.choices

    provider_long_name = forms.CharField(max_length=100)
    base_url = forms.URLField()

    property_list = forms.CharField(widget=forms.Textarea)
    approved_sets = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url',
                  'property_list', 'approved_sets']


class OtherProviderForm(ModelForm):
    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'property_list']
