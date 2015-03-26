from django import forms
from provider_registration.validators import URLResolves


from provider_registration.models import RegistrationInfo


class ContactInfoForm(forms.ModelForm):

    class Meta:
        model = RegistrationInfo
        fields = ['contact_name', 'contact_email']


class MetadataQuestionsForm(forms.ModelForm):
    reg_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['meta_tos', 'meta_rights', 'meta_privacy', 'meta_sharing',
                  'meta_license_cc0', 'reg_id']


class InitialProviderForm(forms.ModelForm):
    base_url = forms.CharField(max_length=100, validators=[URLResolves()])
    reg_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'description', 'oai_provider',
                  'reg_id', 'rate_limit', 'api_docs']


class OAIProviderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(OAIProviderForm, self).__init__(*args, **kwargs)
        self.fields['approved_sets'].choices = self.choices

    property_list = forms.CharField(widget=forms.HiddenInput)
    reg_id = forms.CharField(widget=forms.HiddenInput())
    provider_long_name = forms.CharField(widget=forms.HiddenInput())
    base_url = forms.URLField()

    approved_sets = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url',
                  'property_list', 'approved_sets', 'reg_id']


class SimpleOAIProviderForm(forms.ModelForm):
    reg_id = forms.CharField(widget=forms.HiddenInput())
    property_list = forms.CharField(widget=forms.HiddenInput)
    provider_long_name = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'reg_id', 'approved_sets', 'property_list']


class OtherProviderForm(forms.ModelForm):
    reg_id = forms.CharField(widget=forms.HiddenInput())
    property_list = forms.CharField(widget=forms.HiddenInput)
    provider_long_name = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'reg_id', 'property_list']
