from django import forms


YES_NO_CHOICES = (
    ('Y', 'yes'),
    ('N', 'no')
)


class ListField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')


class ProviderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(ProviderForm, self).__init__(*args, **kwargs)
        self.fields['approved_sets'].choices = self.choices

    provider_long_name = forms.CharField(max_length=100)
    provider_short_name = forms.CharField(max_length=50)
    base_url = forms.URLField()

    property_list = forms.CharField(widget=forms.Textarea)
    approved_sets = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    # def to_python(self, value):
    #     "Normalize data to a list of strings"

    # def is_valid(self):
    #     pass


class InitialProviderForm(forms.Form):
    provider_long_name = forms.CharField(max_length=100)
    provider_short_name = forms.CharField(max_length=50)
    base_url = forms.URLField()
    description = forms.CharField(widget=forms.Textarea)

    # Terms of Service and Metadata Permissions Questions
    meta_tos = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES)
    meta_privacy = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES)
    meta_sharing_tos = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES)
    meta_license = forms.CharField(max_length=50)
    meta_license_extended = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES)
    meta_future_license = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES)
