from django import forms
from provider_registration.validators import ValidOAIURL, URLResolves


from provider_registration.models import RegistrationInfo


class InitialProviderForm(forms.ModelForm):
    base_url = forms.CharField(max_length=100, validators=[URLResolves()])

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'description',
                  'oai_provider', 'meta_tos', 'meta_privacy', 'meta_sharing_tos',
                  'meta_license', 'meta_license_extended', 'meta_future_license',
                  'contact_name', 'contact_email']


class OAIProviderForm(forms.ModelForm):
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

        validators = [ValidOAIURL()]


class OtherProviderForm(forms.ModelForm):
    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'property_list']
