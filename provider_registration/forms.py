from django import forms


class ListField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')


class ProviderForm(forms.Form):
    provider_name = forms.CharField(max_length=50)
    base_url = forms.URLField()
    property_list = forms.CharField(widget=forms.Textarea)
    # approved_sets = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    approved_sets = forms.CharField(widget=forms.Textarea)

    # def to_python(self, value):
    #     "Normalize data to a list of strings"

    # def is_valid(self):
    #     pass


class InitialProviderForm(forms.Form):
    provider_name = forms.CharField(max_length=50)
    base_url = forms.URLField()
