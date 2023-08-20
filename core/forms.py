from django import forms


class SearchForm(forms.Form):
    name = forms.CharField(required=True,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control rounded search',
                                    'placeholder': 'Axtar...'
                                }))
